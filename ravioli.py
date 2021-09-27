#! /usr/bin/env python

from art import tprint

import pasta.siakad_auto_attendance.main

def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values

def say_welcome():
    tprint("{*} RAVIOLI")

def ask_auto_absen():
    return yn_choice("Start 'auto-absen' sequence")

if __name__ == '__main__':
    say_welcome()
    if ask_auto_absen():
        pasta.siakad_auto_attendance.main.start()
