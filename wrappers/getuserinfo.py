from wrappers.baserequestwrapper import BaseRequestWrapper

class GetUserInfo(BaseRequestWrapper):
    """
    Wrapper for the GetUserInfo GraphQL query.

    This query allows us to get all workouts ending at a date (to) for a given range of 3, 6, 8, 12, 16 weeks back. 
    For example, a "to" date of 2021-10-04 and a range of 3, will give us all workouts from 2021-09-13 to 2021-10-04.
    """
    query = {
        "operationName": "GetUserInfo", 
        "variables": {
            "userInfoUname": ""
        },
        "query": "query GetUserInfo($userInfoUname: String!) {\n  userInfo(uname: $userInfoUname) {\n    user {\n      ...UserFields\n      __typename\n    }\n    daysLogged\n    best3 {\n      w\n      e {\n        id\n        name\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserFields on User {\n  id\n  avatarhash\n  uname\n  cc\n  slvl\n  sok\n  age\n  bw\n  private\n  isf\n  joined\n  usekg\n  custom1RM\n  est1RMFactor\n  jranges\n  estimate1RMFormula\n  __typename\n}\n"
    }

    def __init__(self, username: str):
        super().__init__()
        #TODO - Parameters validation

        self.username = username
        self.query["variables"]["userInfoUname"] = self.username
        
    def get(self):
        # TODO multiple queries necessary here because of the range variable limitation
        # loop and modify the query variables
        # check schema first to make sure there's not other way
        super().get()

    def parse(self):
        self.user_id = self.data['userInfo']["user"]["id"]
        