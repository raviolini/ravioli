import plyer.platforms.win.notification
from plyer import notification

"""def create_toaster():
    toaster = ToastNotifier()
    return toaster """

def show_toaster(message = "this is default message"):
    notification.notify("Alarm Reminder", message)

if __name__ == "__main__":
    show_toaster("Saatnya absen")
