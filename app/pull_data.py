import requests, json
from geopy.geocoders import Nominatim

def get_data(lat, lng, api_key):
    # Enter your API key here

    #geolocator = Nominatim(timeout=10)
    #location = geolocator.geocode(city)
    #lat = location.latitude
    #lng = location.longitude

    # base_url variable to store url
    base_url = f'https://api.darksky.net/forecast/{api_key}/{lat},{lng}?units=si'

    #base_url = "http://api.openweathermap.org/data/2.5/weather?" +"lat=" +str(lat)+ "&lon=" +str(lng) + "&appid=" + api_key


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

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found

    description_current = x["currently"]["summary"]
    description_day = x["hourly"]["summary"]
    current_temperature = x["currently"]["temperature"]
    feels_like = x["currently"]["apparentTemperature"]
    min_temperature = x["daily"]["data"][0]["temperatureLow"]
    max_temperature = x["daily"]["data"][0]["temperatureHigh"]
    humidity = x["daily"]["data"][0]["humidity"] * 100
    return description_current, description_day, current_temperature, feels_like, min_temperature, max_temperature, humidity
