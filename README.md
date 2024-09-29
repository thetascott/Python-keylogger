# Python-keylogger

**This project is a proof of concept for educational purposes and improvements can be made.**

This keylogger saves keystrokes to a text file, saves the client's system information, and saves a screenshot of the desktop every 15 seconds.  The keystroke and system information files are encrypted.  The text files and screenshots are e-mailed at set intervals.  

To run the application:
1.  Run `python cryptography/generateKey.py` which saves the key to a text file.
2.  Set the email_address, password, file_path and key variables.  Set the key to the value generated in step 1.
3.  Run `python logger.py`.
