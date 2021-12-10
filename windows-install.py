"""
simple script to "install" the ravioli, it just put the absen startup in the startup folder
"""

if __name__ == "__main__":
    import os
    import sys
    import subprocess

    #targeted file
    target_file = "absen-startup.exe"

    #print target_file if exist
    if os.path.isfile(target_file):
        print("[+] file found")

    #startup folder
    startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    print("your startup folder : ", startup_folder)

    #get the current path of targeted file
    target_file = os.path.abspath(target_file)

    #create shortcut from targeted file
    try:
        subprocess.call(["cmd", "/c", "mklink", "/J", os.path.join(startup_folder, "absen-startup.lnk"), target_file])
        print("[+] shortcut created")
    except Exception as e:
        print(e)
        sys.exit(1)

    print("[+] done")

    print("ravioli installed")
    input("press enter to exit")


    

    