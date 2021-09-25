import os


def config_credential():
    try:
        os.system("python -m pasta.siakad_auto_attendance.configure")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    config_credential()