from datetime import date
from datetime import time

def parse_date(date_string):
  return date.fromisoformat(date_string)

def parse_time(time_string):
  if time_string:
    return time.fromisoformat(time_string)

