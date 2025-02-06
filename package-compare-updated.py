import pandas as pd

def extract_package_names(package_list):
    """Extract only package names, ignoring version numbers."""
    return {pkg.split('-')[0] for pkg in package_list}

# Load package lists
rhel7_file = "rhel7_packages.txt"
rhel8_file = "rhel8_packages.txt"

# Read package lists into sets
with open(rhel7_file, "r") as file:
    rhel7_packages = file.read().splitlines()

with open(rhel8_file, "r") as file:
    rhel8_packages = file.read().splitlines()

# Extract package names
rhel7_package_names = extract_package_names(rhel7_packages)
rhel8_package_names = extract_package_names(rhel8_packages)

# Create a comparison list based only on RHEL7
data = []
for package in sorted(rhel7_package_names):
    rhel7_value = package
    rhel8_value = package if package in rhel8_package_names else "Not Installed"
    data.append([rhel7_value, rhel8_value])

# Create DataFrame for the output
df = pd.DataFrame(data, columns=["RHEL7 Packages", "RHEL8 Packages"])

# Write to Excel
output_file = "rpm_comparison_rhel7_vs_rhel8.xlsx"
df.to_excel(output_file, index=False)

print(f"Comparison completed. Results saved in {output_file}.")
