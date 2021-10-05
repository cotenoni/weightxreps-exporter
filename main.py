import requests
import json
import settings
from JRangeGetter import JRangeGetter

class CalendarDaysGetter:
    def __init__(self, f, to):
        self.calendar_days = None
        self.f = f
        self.to = to
        self.query = {
            "operationName":"GetCalendarDays",
            "variables":{"uid":"4090","from":self.f,"to":self.to},
            "query":"query GetCalendarDays($uid: ID!, $from: YYYYMMDD!, $to: YYYYMMDD!) {\n  getCalendarDays(uid: $uid, from: $from, to: $to)\n}\n"
        }

    def get_calendar_days(self):
        r = requests.post(settings.URL, json=self.query)
        json_data = json.loads(r.text)['data']['getCalendarDays']
        self.calendar_days = [self.__extract_date(s) for s in json_data if self.__is_workout_day(s)]

    def __is_workout_day(self, s: str):
        return s[-1] == "1"

    def __extract_date(self, s: str):
        return s[:len(s) - 1]
    
    
if __name__ == '__main__':
    #TODO - Replace with command line argument
    jr = JRangeGetter("4090", '2021-10-04', 3)
    jr.get_jrange()