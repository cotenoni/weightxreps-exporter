from workouts_handler import WorkoutsHandler
from datetime import datetime
import os

FILENAME_PREFIX = "export/"


if __name__ == '__main__':
    #TODO - Replace with command line argument
    jr = WorkoutsHandler("4090", '2021-10-04', 3)
    jr.get()

    if not os.path.isdir('export'):
        os.mkdir("export")

    filename = FILENAME_PREFIX + str(datetime.now())
    for c in [" ", "-", ":", "."]:
        filename = filename.replace(c, "")
    
    f = open(filename + ".json", 'x')
    f.write(jr.raw)
    f.close()