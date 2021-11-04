import time

import schedule

from flour.event_scheduler.subscriber import use_subscriber, get_subscriber

HEARTBEAT = 2

@use_subscriber
def start(scheduler, **kwargs):
    subscriber = get_subscriber(kwargs)

    subscriber.set_default_scheduler(scheduler)
    subscriber.subscribe_into("flow_control")

    schedule.every().monday.at("06:00:10").do(lambda: scheduler.publish("siakad_auto_attendance", "fill_attendance"))
    schedule.every().tuesday.at("06:00:10").do(lambda: scheduler.publish("siakad_auto_attendance", "fill_attendance"))
    schedule.every().wednesday.at("06:00:10").do(lambda: scheduler.publish("siakad_auto_attendance", "fill_attendance"))
    schedule.every().thursday.at("06:00:10").do(lambda: scheduler.publish("siakad_auto_attendance", "fill_attendance"))
    schedule.every().friday.at("06:00:10").do(lambda: scheduler.publish("siakad_auto_attendance", "fill_attendance"))

    while True:
        task = subscriber.poll_event()

        if task is None:
            pass
        elif task.name == "terminate":
            break;

        schedule.run_pending()
        time.sleep(HEARTBEAT)
