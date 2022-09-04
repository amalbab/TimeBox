import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from authenticate import get_creds
import re


eventsList = []
def onload():
  print("REACHED!!!")
  global creds
  creds = get_creds()

  global service
  service = build('calendar', 'v3', credentials=creds)

  # global eventsList 
  # eventsList = []



def parse_match(match):
  print('MATCH', match)
  event = match[1]

  startHour = int(match[3])
  startMin = match[4]
  startPeriod = match[5]

  endHour = int(match[7])
  endMin = match[8]
  endPeriod = match[9]


  return {
    'event':event,
    'startHour':startHour,
    'startMin':startMin,
    'startPeriod':startPeriod,
    'endHour':endHour,
    'endMin':endMin,
    'endPeriod':endPeriod
  }

import datetime
def formatted_time(matches):
  date = datetime.datetime.now().astimezone()
  curr_hour = date.hour

  sleep_hours = (1, 7)

  startDay = 0
  endDay = 0

  startHour = matches['startHour']
  if matches['startPeriod'] != '':
    startHour = int(matches['startPeriod'].lower() == 'pm')*12 + startHour%12
    # if startHour > 12:
    #   return
    if startHour < curr_hour:
      startDay += 1
  else:
    if startHour < curr_hour:
      startHour += 12
      if startHour > 24:
        startHour % 24
        startDay += 1

     
  endHour = matches['endHour']
  if matches['endPeriod'] != '':
    endHour = int(matches['endPeriod'].lower() == 'pm')*12 + matches['endHour']
    # if endHour > 12:
    #   return
    # print("ENDHOUR", endHour)
    if endHour < startHour or startDay > endDay:
      endDay += 1
  else:
    if startHour > endHour:
      if (endHour + 12)%24 <  startHour:
        endDay += 1
      else:
        endHour += 12
        if endHour > 24:
          endHour %= 24
          endDay += 1


  
  print("HERE ***", startHour, endHour)
  startDate = date + datetime.timedelta(days = startDay)
  endDate = date + datetime.timedelta(days=endDay)


  startMin = matches['startMin']
  endMin = matches['endMin']
  if startMin == '':
    startMin = 0 
  if endMin == '':
    endMin = 0 

  print(startHour)

  startDate = startDate.replace(hour=startHour, minute=int(startMin))
  endDate = endDate.replace(hour=endHour, minute=int(endMin))

  startMins = startDate.hour * 60 + startDate.minute
  endMins = endDate.hour * 60 + endDate.minute

  print('ENDMIN' ,endHour)
  print('STARTMIN', startHour)

  startDate = startDate.isoformat()
  endDate = endDate.isoformat()

  print(startHour)
  print(endHour)
  
  
  return {
    'event':matches['event'],
    'startTime':startDate,
    'endTime':endDate,
    'startMins' : startMins,
    'endMins' : endMins
  }


def extract_data(text):
  # process text first
  time_pattern = r'((.*?)(\sfrom\s)?(\d{2}|\d)(:|\s\d{2})?(AM|PM)?\s?(-|to)\s?(\d{2}|\d)(:|\s\d{2})?(AM|PM)?(.*))'

  # matches = re.findall(time_pattern, text, flags=re.IGNORECASE)

  events_data = []


  for line in text.split('\n'):
    match = re.findall(time_pattern, line, flags = re.IGNORECASE)

    if len(match) == 0:
      event = {
        'summary': line,
      }

    else:
      formatted_match = parse_match(match[0])

      event_format = formatted_time(formatted_match)

      event = {
      'summary': event_format['event'],
      'start': {
        'dateTime': event_format['startTime'],
        'timeZone': 'EST',
      },
      'end': {
        'dateTime': event_format['endTime'],
        'timeZone': 'EST',
      },
      'mins' : {
        'startMin' : event_format['startMins'],
        'endMin' : event_format['endMins']
      }
    }

    # print(eventsList)

    events_data.append(event)

  for event in events_data:
    eventsList.append(event)


  return events_data


def schedule():
  # print('AMALHASARRIVED')

  for event in eventsList:
    print(event)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

  




