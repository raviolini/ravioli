from win10toast import ToastNotifier

def create_toaster():
    toaster = ToastNotifier()
    return toaster

def show_toaster(message = "this is default message"):
    toaster = create_toaster()
    toaster.show_toast("Alarm Reminder",message)

if __name__ == "__main__":
    show_toaster("Saatnya absen")
