from wrappers import GetJRange, GetUserInfo
from datetime import date, datetime, timedelta
import argparse
import os
import json

DIR_NAME = "export"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, help='weightxreps username for whom to export data.')
    parser.add_argument('-s', '--start', type=date.fromisoformat, default=None, help='Start date for the export. Default: 3 weeks ago.')
    parser.add_argument('-e', '--end', type=date.fromisoformat, default=date.today(), help='End date for the export. Default: today.')
    args = parser.parse_args()

    if args.start is not None and args.end <= args.start:
        raise ValueError("End date need to be after start date.",)

    return args

def create_export_dir_if_inexistant():
    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)
    return

def create_and_write_file(file_prefix: str, raw_data: str):
    filename = DIR_NAME + '/' + file_prefix + '_' + str(datetime.now())
    for c in [" ", "-", ":", "."]:
        filename = filename.replace(c, "")
    
    f = open(filename + ".json", 'x')
    f.write(raw_data)
    f.close()


if __name__ == '__main__':
    args = parse_arguments()
    create_export_dir_if_inexistant()
    userInfoWrapper = GetUserInfo(args.username)
    userInfoWrapper.get()
    create_and_write_file("UserInfo", json.dumps(userInfoWrapper.user_info))

    if args.start is None:
        args.start = userInfoWrapper.date_joined

    jr = GetJRange(userInfoWrapper.user_id, args.start, args.end)
    jr.get()
    
    print(f"Saving {len(jr.workouts)} workout(s) to file.")
    if len(jr.workouts) > 0:
        print(f"First workout date : {jr.workouts[0]['on']}")
        print(f"Last workout date : {jr.workouts[len(jr.workouts)- 1]['on']}")

    create_and_write_file("Workouts", json.dumps(jr.workouts))


    