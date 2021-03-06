from wrappers.baserequestwrapper import BaseRequestWrapper
from datetime import datetime

class GetUserInfo(BaseRequestWrapper):
    """
    Wrapper for the GetUserInfo GraphQL query.

    This query allows us to get all the user informations based on it's username. 
    """
    query = {
        "operationName": "GetUserInfo", 
        "variables": {
            "userInfoUname": ""
        },
        "query": "query GetUserInfo($userInfoUname: String!) {\n  userInfo(uname: $userInfoUname) {\n    user {\n      ...UserFields\n          }\n    daysLogged\n    best3 {\n      w\n      e {\n        id\n        name\n        type\n              }\n          }\n      }\n}\n\nfragment UserFields on User {\n  id\n  avatarhash\n  uname\n  cc\n  slvl\n  sok\n  age\n  bw\n  private\n  isf\n  joined\n  usekg\n  custom1RM\n  est1RMFactor\n  jranges\n  estimate1RMFormula\n  }\n"
    }

    def __init__(self, username: str):
        super().__init__()
        #TODO - Parameters validation

        self.username = username
        self.query["variables"]["userInfoUname"] = self.username

    def parse(self):
        self.user_id = self.data['userInfo']["user"]["id"]
        self.user_info = self.data['userInfo']
        self.date_joined = datetime.strptime(self.user_info['user']['joined'], "%a, %d %b %Y %H:%M:%S %Z").date()
        
        