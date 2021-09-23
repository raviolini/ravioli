import time
import datetime

def get_time_now():
    now = datetime.datetime.now()
    return now

def get_hour():
    return get_time_now().hour

def waktu_absen():
    hour = get_hour()
    if hour >= 6 and hour <=9: #NICE
        return True
    return False

if __name__ == '__main__':
    print(waktu_absen())
