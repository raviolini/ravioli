from flour.event_scheduler.subscriber import use_subscriber, get_subscriber

from . import tasks

@use_subscriber
def start(scheduler, **kwargs):
    subscriber = get_subscriber(kwargs)

    subscriber.set_default_scheduler(scheduler)
    subscriber.subscribe_into("siakad_auto_attendance")
    subscriber.subscribe_into("flow_control")

    while True:
        task = subscriber.wait_event()

        if task is None:
            continue
        elif task.name == "fill_attendance":
            tasks.fill_attendance()
        elif task.name == "sign_in":
            tasks.sign_in()
        elif task.name == "configure":
            tasks.configure()
        elif task.name == "clean_login_information":
            tasks.clean_login_information()
        elif task.name == "terminate":
            break;
