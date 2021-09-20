#! /usr/bin/env python
import autoabsen

from halo import Halo
from pyfiglet import Figlet

from os import system
import time

def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values

def say_welcome():
    figlet = Figlet(font='slant')
    print(figlet.renderText('RAVIOLI'))

def download_ram():
    spinner = Halo(text='Downloading RAM', spinner='dots')
    spinner.start()
    time.sleep(2.4)
    spinner.succeed()

def stop_alien_invasion():
    spinner = Halo(text = "Stopping imminent alien invasion", spinner='dots')
    spinner.start()
    time.sleep(2.4)
    spinner.succeed()

def hide_homework_folder():
    spinner = Halo(text = "Hiding homework folder", spinner='dots')
    spinner.start()
    time.sleep(2.4)
    spinner.succeed()

def ask_auto_absen():
    return yn_choice("Start 'auto-absen' sequence")

def start_neofetch():
    system('neofetch')

if __name__ == '__main__':
    say_welcome()
    #download_ram()
    #stop_alien_invasion()
    #hide_homework_folder()
    if ask_auto_absen():
        autoabsen.start()
