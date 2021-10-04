import requests
import json

URL = "https://weightxreps.net/wxr-server-2/graphql"

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
        r = requests.post(URL, json=self.query)
        json_data = json.loads(r.text)['data']['getCalendarDays']
        self.calendar_days = [self.__extract_date(s) for s in json_data if self.__is_workout_day(s)]

    def __is_workout_day(self, s: str):
        return s[-1] == "1"

    def __extract_date(self, s: str):
        return s[:len(s) - 1]
    

class JRangeGetter:
    def __init__(self, f: str, range: int):
        self.f = f
        self.range = range #The API only seems to support the following values 3, 6, 8, 12, 16
        self.query = {
            "operationName": "GetJRange",
            "variables": {
                "uid": "4090",
                "ymd": self.f,
                "range": self.range
            },
            "query": "query GetJRange($uid: ID!, $ymd: YMD!, $range: Int!) {\n  jrange(uid: $uid, ymd: $ymd, range: $range) {\n    exercises {\n      id\n      name\n      type\n      __typename\n    }\n    days {\n      on\n      did {\n        eid\n        sets {\n          w\n          r\n          s\n          lb\n          ubw\n          c\n          rpe\n          pr\n          est1rm\n          eff\n          int\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        self.jdays = None

    def get_jrange(self):
        r = requests.post(URL, json=self.query)
        print(r.status_code)
        print(r.text)
        json_data = json.loads(r.text)['data']['jrange']
        exercises = json_data['exercises']
        workouts = json_data['days']

        workouts = [self.add_exercise_to_workout(workout, exercises) for workout in workouts]
        print(workouts)

        #print(self.calendar_days)

    def add_exercise_to_workout(self, workout, exercises):
        for exercise in workout["did"]:
            exercise["exercise"] = next(filter(lambda e: e["id"] == exercise["eid"], exercises))
        return workout


if __name__ == '__main__':
    #TODO - Replace with command line argument
    f = '20210822'
    to = '20211004'
    cd = CalendarDaysGetter(f, to)
    cd.get_calendar_days()

    jr = JRangeGetter('2021-10-04', 16)
    jr.get_jrange()