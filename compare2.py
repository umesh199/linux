import pandas as pd

# Load package lists
rhel7_file = "rhel7_packages.txt"
rhel8_file = "rhel8_packages.txt"

# Read package lists
with open(rhel7_file, "r") as file:
    rhel7_packages = set(file.read().strip().splitlines())

with open(rhel8_file, "r") as file:
    rhel8_packages = set(file.read().strip().splitlines())

# Prepare comparison data
data = []
for package in sorted(rhel7_packages):
    if package in rhel8_packages:
        rhel8_status = package
    else:
        rhel8_status = "Available in RHEL7 but not installed in RHEL8"
    data.append([package, rhel8_status])

# Create a DataFrame
df = pd.DataFrame(data, columns=["RHEL7 Packages", "RHEL8 Status"])

# Write to Excel
output_file = "rpm_comparison_rhel7_vs_rhel8.xlsx"
df.to_excel(output_file, index=False)

print(f"Comparison completed. Results saved in {output_file}.")
