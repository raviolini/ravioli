from PIL import Image
from pystray import Icon, Menu, MenuItem

from flour.event_scheduler.scheduler import Scheduler

def start(scheduler: Scheduler):
    def terminate():
        scheduler.publish("flow_control", "terminate")
        icon.stop()

    icon_image = Image.open("sauce/favicon.ico")

    icon = Icon("Rierogi", icon_image, menu=Menu(
        MenuItem("Fill Attendance", lambda: scheduler.publish("siakad_auto_attendance", "fill_attendance")),
        MenuItem("Sign In", lambda: scheduler.publish("siakad_auto_attendance", "sign_in")),
        MenuItem("Configure", lambda: scheduler.publish("siakad_auto_attendance", "configure")),
        MenuItem("Exit", terminate)
    ))

    icon.run()
