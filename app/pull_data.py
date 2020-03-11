import requests, json
from geopy.geocoders import Nominatim

def get_data(lat, lng, api_key):
    # Enter your API key here

    #geolocator = Nominatim(timeout=10)
    #location = geolocator.geocode(city)
    #lat = location.latitude
    #lng = location.longitude

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?" +"lat=" +str(lat)+ "&lon=" +str(lng) + "&appid=" + api_key


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
    if x["cod"] != "404":

        description = x["weather"][0]["description"]
        current_temperature = x["main"]["temp"]
        min_temperature = x["main"]["temp_min"]
        max_temperature = x["main"]["temp_max"]
        feels_like = x["main"]["feels_like"]



        return description, current_temperature, min_temperature, max_temperature, feels_like
    else:
        print(" City Not Found ")
