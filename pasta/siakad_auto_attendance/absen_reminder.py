import datetime

def get_time_now():
    now = datetime.datetime.now()
    return now

def get_hour():
    return get_time_now().hour

def waktu_absen():
    return 6 <= get_hour() <= 9

if __name__ == '__main__':
    print(waktu_absen())
