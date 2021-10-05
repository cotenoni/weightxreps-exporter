import requests
import json
from workouts_handler import WorkoutsHandler


if __name__ == '__main__':
    #TODO - Replace with command line argument
    jr = WorkoutsHandler("4090", '2021-10-04', 3)
    jr.get()
    print(jr.workouts)