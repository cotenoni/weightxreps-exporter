from wrappers.baserequestwrapper import BaseRequestWrapper

class GetUserInfo(BaseRequestWrapper):
    """
    Wrapper for the GetUserInfo GraphQL query.

    This query allows us to get all workouts ending at a date (to) for a given range of 3, 6, 8, 12, 16 weeks back. 
    For example, a "to" date of 2021-10-04 and a range of 3, will give us all workouts from 2021-09-13 to 2021-10-04.
    """
    