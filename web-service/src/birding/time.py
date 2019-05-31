from datetime import datetime
from datetime import timedelta

def get_current_time(minutesoffset=None):
  time = datetime.utcnow()
  if minutesoffset:
    return time + timedelta(minutes=minutesoffset)
  else:
    return time
