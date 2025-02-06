import pandas as pd

def extract_package_names(package_list):
    # Extract only the package names, ignoring version numbers
    package_names = {pkg.split('-')[0] for pkg in package_list}
    return package_names

# Load package lists
rhel7_file = "rhel7_packages.txt"
rhel8_file = "rhel8_packages.txt"

# Read package lists into sets
with open(rhel7_file, "r") as file:
    rhel7_packages = file.read().splitlines()

with open(rhel8_file, "r") as file:
    rhel8_packages = file.read().splitlines()

# Extract only package names
rhel7_package_names = extract_package_names(rhel7_packages)
rhel8_package_names = extract_package_names(rhel8_packages)

# Find matching and non-matching packages
matching_packages = list(rhel7_package_names.intersection(rhel8_package_names))
non_matching_rhel7 = list(rhel7_package_names - rhel8_package_names)
non_matching_rhel8 = list(rhel8_package_names - rhel7_package_names)

# Create DataFrames for better Excel formatting
matching_df = pd.DataFrame(matching_packages, columns=["Matching Packages"])
non_matching_rhel7_df = pd.DataFrame(non_matching_rhel7, columns=["RHEL7 Only Packages"])
non_matching_rhel8_df = pd.DataFrame(non_matching_rhel8, columns=["RHEL8 Only Packages"])

# Write to Excel
with pd.ExcelWriter("rpm_comparison_results_ignore_versions.xlsx") as writer:
    matching_df.to_excel(writer, sheet_name="Matching Packages", index=False)
    non_matching_rhel7_df.to_excel(writer, sheet_name="RHEL7 Only Packages", index=False)
    non_matching_rhel8_df.to_excel(writer, sheet_name="RHEL8 Only Packages", index=False)

print("Comparison completed. Results saved in rpm_comparison_results_ignore_versions.xlsx.")
