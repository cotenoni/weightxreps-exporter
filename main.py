from workoutshandler import WorkoutsHandler
from datetime import date, datetime, timedelta
import argparse
import os

FILENAME_PREFIX = "export/"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', type=str, help='weightxreps user id. Can be found by looking at GraphQL query made when accessing the user profile.')
    parser.add_argument('-s', '--start', type=date.fromisoformat, default=date.today() - timedelta(days=21), help='Start date for the export. Default: 3 weeks ago.')
    parser.add_argument('-e', '--end', type=date.fromisoformat, default=date.today(), help='End date for the export. Default: today.')
    args = parser.parse_args()

    if args.end <= args.start:
        raise ValueError("End date need to be after start date.",)

    return args

def create_export_dir_if_inexistant():
    if not os.path.isdir('export'):
        os.mkdir("export")
    return

def create_and_write_file(raw_data: str):
    filename = FILENAME_PREFIX + str(datetime.now())
    for c in [" ", "-", ":", "."]:
        filename = filename.replace(c, "")
    
    f = open(filename + ".json", 'x')
    f.write(raw_data)
    f.close()


if __name__ == '__main__':
    args = parse_arguments()
    create_export_dir_if_inexistant()

    print(args.uid)
    print(args.start)
    print(args.end)

    jr = WorkoutsHandler("4090", '2021-10-04', 3)
    jr.get()
    create_and_write_file(jr.raw)


    