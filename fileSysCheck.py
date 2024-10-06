import os
import pandas as pd
import subprocess

# Check if the directory exists
def check_directory(directory_path):
    return os.path.exists(directory_path)

# Read directories from an Excel file
def read_directories_from_excel(excel_file_path):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path)
        # Ensure the column 'Directory' is present
        if 'Directory' not in df.columns:
            print("Excel file must contain a 'Directory' column.")
            return []
        # Return list of directories
        return df['Directory'].tolist()
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return []

# Send email notification using sendmail
def send_email(to_address, subject, body):
    from_address = "your_email@example.com"  # Replace with your email or system email

    # Create the email message
    message = f"""From: {from_address}
To: {to_address}
Subject: {subject}

{body}
"""

    # Use subprocess to call sendmail
    try:
        process = subprocess.Popen(['/usr/sbin/sendmail', '-t', '-oi'], stdin=subprocess.PIPE)
        process.communicate(message.encode('utf-8'))
        print(f"Email sent to {to_address} successfully!")
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

# Main function to check directories and send email if missing
def main():
    excel_file_path = "directories_list.xlsx"  # Replace with the path to your Excel file
    alert_email = "recipient@example.com"      # Email to send notifications to
    
    # Step 1: Read directories from the Excel file
    directory_list = read_directories_from_excel(excel_file_path)
    
    if not directory_list:
        print("No directories found in the Excel file.")
        return
    
    # Step 2: Check if each directory exists
    for directory_path in directory_list:
        if not check_directory(directory_path):
            print(f"Directory '{directory_path}' is missing!")
            
            # Step 3: Send email if directory is missing
            subject = "Directory Missing Alert"
            body = f"The directory '{directory_path}' is missing. Please check the system."
            send_email(alert_email, subject, body)
        else:
            print(f"Directory '{directory_path}' exists.")

if __name__ == "__main__":
    main()
