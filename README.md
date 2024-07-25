###Keylogger and Encryption Tool
##Project Description
This project is a keylogger that captures keystrokes, encrypts the captured data using the Fernet encryption algorithm, and sends the encrypted data along with the encryption key via email. The tool demonstrates keylogging, data encryption, and secure data transmission using Python.

Features
Keylogging: Captures all keystrokes on the system.
Data Encryption: Encrypts the captured keystrokes using Fernet symmetric encryption.
Email Transmission: Sends the encrypted log file and the encryption key via email.
Installation and Setup
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/keylogger-encryption-tool.git
Navigate to the Project Directory:

bash
Copy code
cd keylogger-encryption-tool
Install Dependencies:
Ensure you have pip installed, then run:

bash
Copy code
pip install -r requirements.txt
Configure Email Settings:
Open the keylogger.py file and update the email_address and password variables with your email credentials.

Run the Keylogger:

bash
Copy code
python keylogger.py
How to Use
The keylogger will start running and capture keystrokes.
Press the ESC key to stop logging keystrokes.
The captured data will be encrypted and saved as encrypted_file.
The encryption key will be saved as secret.key.
Both files will be sent to the specified email address.
License
This project is licensed under the MIT License. See the LICENSE file for details.
