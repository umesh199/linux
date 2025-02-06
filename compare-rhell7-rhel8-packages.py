import pandas as pd

# Load package lists
rhel7_file = "rhel7_packages.txt"
rhel8_file = "rhel8_packages.txt"

# Read package lists into sets (keeping full package names)
with open(rhel7_file, "r") as file:
    rhel7_packages = set(file.read().strip().splitlines())

with open(rhel8_file, "r") as file:
    rhel8_packages = set(file.read().strip().splitlines())

# Create a comparison DataFrame with all RHEL7 packages
data = []
for package in sorted(rhel7_packages):
    rhel7_value = package
    rhel8_value = package if package in rhel8_packages else "Not Installed"
    data.append([rhel7_value, rhel8_value])

# Create DataFrame for the output
df = pd.DataFrame(data, columns=["RHEL7 Packages", "RHEL8 Packages"])

# Write to Excel
output_file = "rpm_comparison_rhel7_vs_rhel8_all_packages.xlsx"
df.to_excel(output_file, index=False)

print(f"Comparison completed. Results saved in {output_file}.")
