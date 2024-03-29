import pysftp
import os, subprocess, re, sys, glob, configparser, shutil
from datetime import datetime, date, time

source_folder = 'mseed'
destination_folder = 'uploaded'

files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
files = sorted(files)
#print(files)
ini_file_path = 'ftpconfig.ini'
config = configparser.ConfigParser()
config.read(ini_file_path)
username = config.get('sftp', 'username', fallback='')
password = config.get('sftp', 'password', fallback='')
server = config.get('sftp', 'server', fallback='')
path = config.get('sftp', 'path', fallback='')

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
sftp = pysftp.Connection(host=server, username=username, password=password, cnopts=cnopts)
sftp.chdir(path)
for file in files:
    source_path = os.path.join(source_folder, file)
    sftp.put(source_path)
    sftp.chmod(file,666)
    print("Uploaded " + file)
    destination_path = os.path.join(destination_folder, file)
    shutil.move(source_path, destination_path)
    print(source_path + " -> " + destination_path)
sftp.close()
current_date = datetime.now()
for filename in os.listdir(destination_folder):
    filepath = os.path.join(destination_folder, filename)
    modification_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    age_of_file = current_date - modification_time
    if age_of_file.days > 90:
        os.remove(filepath)
        print(f"Deleted: {filename}")
