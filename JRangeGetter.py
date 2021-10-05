import json
import requests
import settings

class JRangeGetter:
    """
    Wrapper for the GetJRange GraphQL query.

    This query allows us to get all workouts ending at a date (to) for a given range of 3, 6, 8, 12, 16 weeks back. 
    For example, a "to" date of 2021-10-04 and a range of 3, will give us all workouts from 2021-09-13 to 2021-10-04.
    """
    query = {
        "operationName": "GetJRange",
        "variables": {
            "uid": "",
            "ymd": "",
            "range": ""
        },
        "query": "query GetJRange($uid: ID!, $ymd: YMD!, $range: Int!) {  jrange(uid: $uid, ymd: $ymd, range: $range) {\n    exercises {\n      id\n      name\n      type\n      __typename\n    }\n    days {\n      on\n      did {\n        eid\n        sets {\n          w\n          r\n          s\n          lb\n          ubw\n          c\n          rpe\n          pr\n          est1rm\n          eff\n          int\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    def __init__(self, user_id: str, to: str, how_many_weeks: int):
        #TODO - Parameters validation

        self.user_id = user_id
        self.to = to
        self.how_many_weeks = how_many_weeks # The query only seems to support the following values 3, 6, 8, 12, 16
        self.query["variables"]["uid"] = self.user_id
        self.query["variables"]["ymd"] = self.to
        self.query["variables"]["range"] = self.how_many_weeks
        self.workouts = []

    def get_jrange(self):
        r = requests.post(settings.URL, json=self.query)
        print(r.status_code)
        print(r.text)
        # TODO Manage status code
        json_data = json.loads(r.text)['data']['jrange']
        exercises = json_data['exercises']
        self.workouts = json_data['days']
        self.workouts = [self.add_exercise_to_workout(workout, exercises) for workout in self.workouts]


    def add_exercise_to_workout(self, workout, exercises):
        for exercise in workout["did"]:
            exercise["exercise"] = next(filter(lambda e: e["id"] == exercise["eid"], exercises))
        return workout