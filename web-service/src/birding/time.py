from datetime import date
from datetime import time

def parse_date(date_string):
  return date.fromisoformat(date_string)

def parse_time(time_string):
  if time_string:
    return time.fromisoformat(time_string)


def format_date_time(date, time=None):
  if time:
    return f'{date.isoformat()} {time.isoformat()}'
  return date.isoformat()
