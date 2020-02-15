from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime, pytz
import time
from datetime import timedelta

def convert_time(city, mail_time):
    geolocator = Nominatim(timeout=10)
    location = geolocator.geocode(city)
    lat = location.latitude
    lng = location.longitude
    tf = TimezoneFinder()
    tmz = tf.timezone_at(lng=lng, lat=lat)
    city_offset = datetime.datetime.now(pytz.timezone(tmz)).strftime('%z')
    server_offset = time.localtime().tm_gmtoff

    city_offset_delta = timedelta(hours = int(city_offset[:3]), minutes=int(city_offset[3:]))
    server_offset_delta = timedelta(seconds=server_offset)
    diff = city_offset_delta - server_offset_delta
    mail_time_delta = timedelta(hours=mail_time)
    new_time = mail_time_delta - diff
    return str(new_time).split(',')[-1].strip()
