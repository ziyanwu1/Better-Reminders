import requests
import api_keys

def get_weather_now(location):
    """
    Returns the weather data at the given location at the current time
    
    Input:
        location: a string to query to the API what location we want the data from. (ex: 'Cambridge,MA,USA')

    Output:
        Returns the weather data in a dictionary (originally from json) format. 
        The API response data fields can be found in https://openweathermap.org/current 

    """

    geo_parameters = {'q':location, 'appid':api_keys.openweather_api}
    geo_r = requests.get('http://api.openweathermap.org/geo/1.0/direct',params=geo_parameters)
    geo_content = geo_r.json()

    latitude = geo_content[0]['lat']
    longitude = geo_content[0]['lon']

    weather_paramters = {'lat':latitude, 'lon':longitude,'appid':api_keys.openweather_api,'units':'metric'}
    weather_r = requests.get("https://api.openweathermap.org/data/2.5/weather",params=weather_paramters)

    return weather_r.json()



def is_raining(weather):
    """
    Returns True/False to see if it's currently raining. Raining includes rain, drizzle, thunderstorms, and snow.
    
    Input:
        weather: weather data (specifically for one instance in time) in the form of the API response (a dictionary json)

    Output:
        A boolean result for whether or not it's raining.

    """

    for conditions in weather['weather']:
        if (conditions['main'] == 'Rain') or (conditions['main'] == 'Drizzle') or (conditions['main'] == 'Thunderstorm') or (conditions['main'] == 'Snow'): 
            return True
    
    return False



def get_weather_five_days(location):
    """
    Returns the weather data in 3 hour blocks at the given location for the next 5 days.
    
    Input:
        location: a string to query to the API what location we want the data from. (ex: 'Cambridge,MA,USA')

    Output:
        Returns the weather data in a dictionary (originally from json) format. 
        The API response data fields can be found in https://openweathermap.org/api/hourly-forecast
        Note the API response json is slightly different from the response from the function that gets only the current weather

    """

    geo_parameters = {'q':location, 'appid':api_keys.openweather_api}
    geo_r = requests.get('http://api.openweathermap.org/geo/1.0/direct',params=geo_parameters)
    geo_content = geo_r.json()

    latitude = geo_content[0]['lat']
    longitude = geo_content[0]['lon']

    weather_paramters = {'lat':latitude, 'lon':longitude,'appid':api_keys.openweather_api,'mode':'json','units':'metric'}
    weather_r = requests.get('http://api.openweathermap.org/data/2.5/forecast',params=weather_paramters)

    return weather_r.json()



def get_weather_block(forecast,block):
    """
    Gets the weather data dictionary for a certain 3-hour block

    Inputs:
        forecast: 5 day weather forecast dictionary from API response
        hour: int in the range [0:39] inclusive

    Output:
        The weather dictionary for that specific time

    """

    return forecast['list'][block]



if __name__ == '__main__':
    location = 'Oakland,CA,USA'
    weather = get_weather_five_days(location)
    next = get_weather_block(weather,0)
    print(is_raining(get_weather_now(location)))
    print(is_raining(next))