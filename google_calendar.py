import os
import datetime
import api_keys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

## TODO: bind timezone to location (possibly get location from the weather) instead of hardcoding it
## 
TIMEZONE = datetime.timezone(datetime.timedelta(hours=-5))


""" When using a service account """
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_service_account.json"

""" Using OAuth but the user has to authenticate every single run """
# flow = InstalledAppFlow.from_client_secrets_file('google_oauth_credentials.json',scopes=["https://www.googleapis.com/auth/calendar.readonly"])
# flow.run_local_server()
# credentials = flow.credentials

""" Trying to use Oauth without having to open the browser every single time """
# Good link: https://stackoverflow.com/questions/73788841/how-to-auto-refresh-google-calendar-token-in-python 

  
credentials = Credentials.from_authorized_user_file('calendar_creds.json')
if not(credentials.valid):
    # If the credentials stored are no longer valid, refresh it
    print('credentials refreshed!')
    
    try:
        credentials.refresh(Request())
    except:
        # For RefreshError, when the refresh token itself expires. We have to manually reauthenticate.
        flow = InstalledAppFlow.from_client_secrets_file('google_oauth_credentials.json',scopes=["https://www.googleapis.com/auth/calendar.readonly"])
        flow.run_local_server()
        credentials = flow.credentials

    # Save the credentials for the next run
    with open('calendar_creds.json','wt') as f:
        f.write(credentials.to_json())


service = build('calendar', 'v3', credentials=credentials)



def get_events(start_date):
    """
    Gets all events whose end times are on that date.
    The phrase "on that day" means that if the event has any part running on that day, it will be included. (even if the event starts or ends outside this date)


    Inputs:
        start_date: A datetime.datetime object (timezone info MUST be included with this object)
    
    Returns:
        Returns a list of events on the calendar. Each event is a dictionary containing information about that event.

    """
    end_date = start_date + datetime.timedelta(days=1)

    events = service.events().list(calendarId = api_keys.my_email ,timeMin=start_date.isoformat(),timeMax=end_date.isoformat()).execute()
    return events['items']



def get_times(events,start_date):
    """
    Returns the start times (hr:min:seconds) of the given events, only if those start times start on the same day as 'start_date'
    
    Inputs:
        events: list of dictionary{str:str}; An event on the Google Calendar is represented by a dictionary, these are the things inside this list
        start_date: A datetime.datetime object
    
    Output:
        Returns a set of the start times for each event. Each start time is a datetime.datetime object

    """
    out = set()

    for event in events:
        event_start_datetime = datetime.datetime.fromisoformat(event['start']['dateTime'])
        consistent_date = event_start_datetime.astimezone(tz=TIMEZONE)
        if consistent_date.day == start_date.day:
            out.add(consistent_date)

    return out


    

if __name__ == '__main__':
    
    # Get's the current day and time in UTC time in the correct format
    # date = datetime.datetime.now(datetime.timezone.utc).isoformat())

    # December 18, 2022 at 12am EST time
    date = datetime.datetime(2022,12,18,tzinfo=TIMEZONE)
    events = get_events(date)
    print(get_times(events,date))
    

    



service.close()