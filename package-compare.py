import pandas as pd

# Load package lists
rhel7_file = "rhel7_packages.txt"
rhel8_file = "rhel8_packages.txt"

# Read package lists into sets
with open(rhel7_file, "r") as file:
    rhel7_packages = set(file.read().splitlines())

with open(rhel8_file, "r") as file:
    rhel8_packages = set(file.read().splitlines())

# Find matching and non-matching packages
matching_packages = list(rhel7_packages.intersection(rhel8_packages))
non_matching_packages_rhel7 = list(rhel7_packages - rhel8_packages)
non_matching_packages_rhel8 = list(rhel8_packages - rhel7_packages)

# Create DataFrames for better Excel formatting
matching_df = pd.DataFrame(matching_packages, columns=["Matching Packages"])
non_matching_rhel7_df = pd.DataFrame(non_matching_packages_rhel7, columns=["RHEL7 Only Packages"])
non_matching_rhel8_df = pd.DataFrame(non_matching_packages_rhel8, columns=["RHEL8 Only Packages"])

# Write to Excel
with pd.ExcelWriter("rpm_comparison_results.xlsx") as writer:
    matching_df.to_excel(writer, sheet_name="Matching Packages", index=False)
    non_matching_rhel7_df.to_excel(writer, sheet_name="RHEL7 Only Packages", index=False)
    non_matching_rhel8_df.to_excel(writer, sheet_name="RHEL8 Only Packages", index=False)

print("Comparison completed. Results saved in rpm_comparison_results.xlsx.")
