import requests
import api_keys

def get_weather():

    ## TODO: Currently, we are hardcoding Cambridge, MA, USA
    geo_parameters = {'q':'Cambridge,MA,USA', 'appid':api_keys.openweather_api}
    geo_r = requests.get('http://api.openweathermap.org/geo/1.0/direct',params=geo_parameters)
    geo_content = geo_r.json()

    latitude = geo_content[0]['lat']
    longitude = geo_content[0]['lon']

    weather_paramters = {'lat':latitude, 'lon':longitude,'appid':api_keys.openweather_api,'units':'metric'}
    weather_r = requests.get("https://api.openweathermap.org/data/2.5/weather",params=weather_paramters)
    print(weather_r.json())


if __name__ == '__main__':
    get_weather()