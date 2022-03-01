from wrappers.baserequestwrapper import BaseRequestWrapper
from datetime import date, timedelta

class GetJRange(BaseRequestWrapper):
    """
    Wrapper for the GetJRange GraphQL query.

    This query allows us to get all workouts between a starting and an ending date (both included).
    """
    query = {
        "operationName": "GetJRange",
        "variables": {
            "uid": "",
            "ymd": "",
            "range": ""
        },
        "query": "query GetJRange($uid: ID!, $ymd: YMD!, $range: Int!) {  jrange(uid: $uid, ymd: $ymd, range: $range) {\n    exercises {\n      id\n      name\n      type\n          }\n    days {\n      on\n      did {\n        eid\n        sets {\n          w\n          r\n          s\n          lb\n          ubw\n          c\n          rpe\n          pr\n          est1rm\n          eff\n          int\n                  }\n              }\n          }\n      }\n}\n"
    }

    def __init__(self, user_id: str, start: date, end: date):
        super().__init__()
        #TODO - Parameters validation

        self.user_id = user_id
        self.start = start
        self.end = end
        
        self.query["variables"]["uid"] = self.user_id
        
        self.query["variables"]["range"] = 12 # The query only seems to support the following values 3, 6, 8, 12, 16
        self.workouts = []

    def get(self):
        # TODO multiple queries necessary here because of the range variable limitation
        # loop and modify the query variables
        # check schema first to make sure there's not other way
        current_end = self.start + timedelta(weeks=12)
        current_start = self.start

        #FIXME : missing workouts because the last query is not made and when we do, we will get more workouts than necessary
        while current_end < self.end:
            self.query["variables"]["ymd"] = current_end.isoformat()
            print(f"Querying from {current_start.isoformat()} to {current_end.isoformat()}")
            super().get()
            current_end = current_end + timedelta(weeks=12) 
            current_start = current_start + timedelta(weeks=12)

    def parse(self):
        jrange = self.data['jrange']

        if jrange is not None:
            self.workouts += [self.add_exercise_info_to_workout(workout, jrange['exercises']) for workout in jrange['days']]

    def add_exercise_info_to_workout(self, workout, exercises):
        for exercise in workout["did"]:
            exercise["exercise"] = next(filter(lambda e: e["id"] == exercise["eid"], exercises))
        return workout