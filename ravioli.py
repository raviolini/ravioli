#! /usr/bin/env python

from threading import Thread

from art import tprint

from flour import log_neko
from pasta.siakad_auto_attendance.main import start as saa_start

from flour.event_scheduler.scheduler import Scheduler as EventScheduler
from flour.event_scheduler.scheduler_task import scheduler_task

import ravioli_systray

if __name__ == '__main__':
    tprint("{*} RAVIOLI")

    log_neko.compose_info("Starting event scheduler");

    event_scheduler = EventScheduler()

    event_scheduler_thread = Thread(
        name="SchedulerThread",
        target=scheduler_task,
        args=[event_scheduler]
    )

    attendance_form_filler_thread = Thread(
        name="SiakadAutoAttendanceThread",
        target=saa_start,
        args=[event_scheduler]
    )

    event_scheduler_thread.start()
    attendance_form_filler_thread.start()

    ravioli_systray.start(event_scheduler)

    attendance_form_filler_thread.join()

    event_scheduler.publish("flow_control", "terminate_scheduler")
    event_scheduler_thread.join()
