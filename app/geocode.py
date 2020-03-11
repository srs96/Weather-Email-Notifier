import requests


def lookup(city, api_key):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='  + city + '&key=' + api_key
    response = requests.get(url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    lat = float(x["results"][0]["geometry"]["location"]["lat"])
    lng = float(x["results"][0]["geometry"]["location"]["lng"])
    return lat, lng
