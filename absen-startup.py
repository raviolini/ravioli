import datetime
import asyncio
import subprocess
import Timer as _timer
import notif_utils
import win32gui, win32con
import os

def get_time_now():
    now = datetime.datetime.now()
    return now

def get_hour():
    return get_time_now().hour

def get_minute():
    return get_time_now().minute

def get_second():
    return get_time_now().second

def waktu_absen():
    return 6 <= get_hour() < 9


async def remind_me():
    timer = _timer.Timer(2, _timer.timeout_callback)  # set timer for two seconds
    while True:
        if waktu_absen():#tinggal ngganti untuk pengaturan waktunya
            await asyncio.sleep(1)  # wait to see timer works
            notif_utils.show_toaster("ABSEN ABSEN") #notification
            break
        else:
            #timer.cancel()
            await asyncio.sleep(1)  # and wait to see it won't call callback
    timer.cancel()#canceling the alarm
    

def _main():
    looper = asyncio.new_event_loop()
    asyncio.set_event_loop(looper)
    try:
        looper.run_until_complete(remind_me())
    finally:
        looper.run_until_complete(looper.shutdown_asyncgens())
        looper.close()

def main(program_name = "ravioli.exe"):
    """
    if you wanna call it from another module, use this main function
    """
    if program_name.endswith(".exe"):
        program = ".\{}".format(program_name)
    else:
        program = "py {}".format(program_name)

    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide , win32con.SW_HIDE)

    _main()

    win32gui.ShowWindow(hide , win32con.SW_SHOW) #reopening the cli
    #ravioli_dummy.main() #change it to your module
    subprocess.Popen(program, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

if __name__ == '__main__':
    main()


