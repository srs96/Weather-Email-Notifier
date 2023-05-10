import requests, json
from geopy.geocoders import Nominatim

def get_data(lat, lng, api_key):
    # Enter your API key here

    #geolocator = Nominatim(timeout=10)
    #location = geolocator.geocode(city)
    #lat = location.latitude
    #lng = location.longitude

    # base_url variable to store url
    #base_url = f'https://api.darksky.net/forecast/{api_key}/{lat},{lng}?units=si'

    print(api_key)
    base_url = "http://api.openweathermap.org/data/2.5/weather?" +"lat=" +str(lat)+ "&lon=" +str(lng) + "&appid=" + api_key +"&units=metric"


    #api.openweathermap.org/data/2.5/weather?lat=35&lon=139

    #city = city.lower()
    #city = city.strip(',')
    #city = [x.strip() for x in city]
    #city = ''.join(e for e in city)
    #city_name = city
    # complete_url variable to store
    # complete url address
    #complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(base_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    print(x)

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    description_current=x["weather"][0]["description"]
    description_day = x["weather"][0]["description"]
    current_temperature = x["main"]["temp"]
    feels_like = x["main"]["feels_like"]
    min_temperature = x["main"]["temp_min"]
    max_temperature = x["main"]["temp_max"]
    humidity = x["main"]["humidity"]
    return description_current, description_day, current_temperature, feels_like, min_temperature, max_temperature, humidity
