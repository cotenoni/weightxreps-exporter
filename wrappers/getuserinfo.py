from wrappers.baserequestwrapper import BaseRequestWrapper

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
        "query": "query GetUserInfo($userInfoUname: String!) {\n  userInfo(uname: $userInfoUname) {\n    user {\n      ...UserFields\n      __typename\n    }\n    daysLogged\n    best3 {\n      w\n      e {\n        id\n        name\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserFields on User {\n  id\n  avatarhash\n  uname\n  cc\n  slvl\n  sok\n  age\n  bw\n  private\n  isf\n  joined\n  usekg\n  custom1RM\n  est1RMFactor\n  jranges\n  estimate1RMFormula\n  __typename\n}\n"
    }

    def __init__(self, username: str):
        super().__init__()
        #TODO - Parameters validation

        self.username = username
        self.query["variables"]["userInfoUname"] = self.username

    def parse(self):
        self.user_id = self.data['userInfo']["user"]["id"]
        