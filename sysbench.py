import csv
import subprocess
import os

def read_hosts_from_inventory(inventory_file):
    """Reads the Ansible inventory file and extracts hostnames."""
    hosts = []
    with open(inventory_file, mode='r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('['):  # Skip group headers
                hosts.append(line)
    return hosts

def run_ansible_playbook():
    """Runs an Ansible playbook to execute sysbench tests on remote hosts."""
    playbook_content = """
    - hosts: all
      gather_facts: yes
      tasks:
        - name: Install sysbench
          apt:
            name: sysbench
            state: present
          become: yes

        - name: Get CPU Core Count
          command: nproc
          register: cpu_cores

        - name: Run CPU Benchmark with Different Core Combinations
          shell: |
            for cores in 1 {{ cpu_cores.stdout }}; do
              sysbench cpu --threads=$cores --cpu-max-prime=20000 run >> /tmp/cpu_results_$cores.txt
            done
          register: cpu_result

        - name: Run Memory Benchmark
          command: sysbench memory run
          register: memory_result

        - name: Run Disk Benchmark
          command: sysbench fileio --file-total-size=1G prepare

        - name: Run Disk I/O Test with Different Modes
          shell: |
            for mode in seqwr seqrd randwr randrd; do
              sysbench fileio --file-total-size=1G --file-test-mode=$mode run >> /tmp/disk_results_$mode.txt
            done
          register: disk_result

        - name: Cleanup Disk Test Files
          command: sysbench fileio cleanup

        - name: Save Results
          copy:
            content: "CPU:\n{{ cpu_result.stdout }}\nMemory:\n{{ memory_result.stdout }}\nDisk:\n{{ disk_result.stdout }}"
            dest: /tmp/sysbench_results.txt
    """
    with open("sysbench_playbook.yml", "w") as file:
        file.write(playbook_content)
    
    subprocess.run(["ansible-playbook", "-i", "inventory", "sysbench_playbook.yml"], check=True)

def collect_results(hosts):
    """Fetches results from remote hosts and writes them to a CSV file."""
    results = []
    for host in hosts:
        output = subprocess.run(["ansible", host, "-m", "fetch", "-a", "src=/tmp/sysbench_results.txt dest=./results/{{inventory_hostname}}.txt flat=yes"], capture_output=True, text=True)
        with open(f"results/{host}.txt", "r") as f:
            data = f.read()
            results.append([host, data])
    
    with open("sysbench_report.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Host", "Benchmark Results"])
        writer.writerows(results)

def main():
    inventory_file = "inventory"
    hosts = read_hosts_from_inventory(inventory_file)
    run_ansible_playbook()
    collect_results(hosts)
    print("Performance analysis completed. Results saved in sysbench_report.csv")

if __name__ == "__main__":
    main()
