import weather
import google_calendar
import emailing
import email.message
import datetime


def get_times_today():
    today = datetime.datetime.now(tz=google_calendar.TIMEZONE)
    date = datetime.datetime(today.year,today.month,today.day,tzinfo=today.tzinfo)

    events = google_calendar.get_events(date)
    times = google_calendar.get_times(events,date)

    return times


def get_notification_times(times):
    """
    Returns the times at which the reminder notifications should be sent out
    As of now, this is 30 minutes before the start time of the event

    Input:
        times: a set of datetime.datetime objects
    
    Output:
        a set of datetime.datetime objects 

    """
    out = set()

    for time in times:
        new_time = time + datetime.timedelta(seconds = -1800)
        out.add(new_time)

    return out


def time_to_alert(times):
    """
    Returns whether or not it is time to send a notification for an approaching event, given a set of times to alert

    Input:
        times: a set of datetime.datetime objects
    
    Output:
        A boolean True/False

    """

    now = datetime.datetime.now(tz=google_calendar.TIMEZONE)
    date = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,tzinfo=now.tzinfo)
    
    if date in times:
        return True
    else:
        return False



def format_message(raining):

    rain_word = "" if raining is True else "Don't "
    second_rain_word = "" if raining is True else "NOT "

    message = email.message.Message()
    message['From'] = 'Better Reminders'
    message['Subject'] = '%sBring Your Umbrella!' % rain_word

    message.set_payload('It is %sraining now!' % second_rain_word) 

    return message.as_string()



def run_weather_notification(notification_times,location):
    """
    This is our main function that runs the entire weather module, does one singular check
    
    Inputs:
        notification_times: times should be gotten from a daily clock
    
    """
    
    if time_to_alert(notification_times) is True:
        
        current_weather = weather.get_weather_now(location)
        
        five_day_weather = weather.get_weather_five_days(location)
        next_weather_block = weather.get_weather_block(five_day_weather,0)

        if weather.is_raining(current_weather) or weather.is_raining(next_weather_block):
            raining = True
        else:
            raining = False
            
        msg = format_message(raining)
        emailing.send_email(msg)



if __name__ == '__main__':
    events = get_times_today()
    times = get_notification_times(events)

    run_weather_notification(times,'Oakland,CA,USA')
    