from enum import Enum

ENDPOINTS = {
    "welcome_page": "https://siswa.smktelkom-mlg.sch.id/welcome",
    "presence_status": "https://siswa.smktelkom-mlg.sch.id/welcome/get_status_hadir",
    "presence_fill": "https://siswa.smktelkom-mlg.sch.id/presnow/chsts",
    "presence_page": "https://siswa.smktelkom-mlg.sch.id/presnow",
    "login": "https://siswa.smktelkom-mlg.sch.id/login/act_login"
}

class Dalu(Enum):
    """ Dalu enum for choosing between Daring and Luring """
    DARING = 0
    LURING = 1
