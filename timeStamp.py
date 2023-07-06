from datetime import timedelta, date
import time

def get_timestamp_interval():
    today = date.today()
    yest = date.today() - timedelta(days=1)
    ts_today = time.mktime(today.timetuple())
    ts_yest = time.mktime(yest.timetuple())
    return str(int(ts_yest*1000)),str(int(ts_today*1000))

#print(get_timestamp_interval())