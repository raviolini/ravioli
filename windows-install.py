"""
simple script to "install" the ravioli, it just put the absen startup in the startup folder
"""

if __name__ == "__main__":
    import os
    import sys
    import shutil
    import subprocess
    import platform
    import time

    # get the path of target script
    target_path = "./absen-startup.exe"

    shortcut = "./absen-startup.lnk"

    # get the path to startup folder
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    # get the path to shortcut
    shortcut_path = os.path.join(startup_folder, shortcut)
    # get the path to target file
    target_path = os.path.join(startup_folder, target_path)

    # if file already exist
    if os.path.exists(shortcut_path):
        print("file already exist")
        sys.exit(1)
    # if not
    else:
        # create folder if not exist
        if not os.path.isdir(startup_folder):
            os.makedirs(startup_folder)
        # create link
        subprocess.call(['C:\Windows\System32\cmd.exe', '/c', 'mklink', '/D', shortcut_path, target_path])
        # check if shortcut exist
        if os.path.exists(shortcut_path):
            print("shortcut created")
            sys.exit(0)
        else:
            print("failed to create shortcut")
            sys.exit(1)

    