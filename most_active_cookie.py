import sys
import logging
import argparse
from datetime import datetime
from collections import defaultdict

class most_active_cookie():
    def __init__(self):
        """Initialize data structure and logger"""

        # {"date": {"cookieName": count}}
        self.dateMap = defaultdict(lambda: defaultdict(int)) 
        self.log = logging.getLogger("most_active_cookie")
            
    def read_file(self, filepath: str) -> None:
        """Read the logs into memory as a dateMap"""

        with open(filepath, "r") as f:
            assert (next(f)=="cookie,timestamp\n"), \
                "First line of logs must be column names = cookie,timestamp"
            line_number = 2
            for line in f:
                items = line.split(",")
                if len(items)!=2:
                    self.log.info(f"Invalid number of columns at row {line_number}. Skipped.")
                # ensuring format of cookie names
                elif not items[0].isalnum() or len(items[0])!=16:
                    self.log.info(f"Cookie name error at line {line_number}. Skipped.")
                else:
                    try:
                        # using string single date as key
                        formattedDate = str(datetime.strptime(items[1].strip(), r"%Y-%m-%dT%H:%M:%S%z").date())
                        self.dateMap[formattedDate][items[0]] += 1
                    except:
                        self.log.info(f"Date format error at line {line_number}. Skipped.")
                line_number += 1
        self.log.info("Logs read into memory")

    def printMostActive(self, date: str) -> None:
        """Scan the unique cookies on given day and print Most Active Cookies"""

        formattedDate = str(datetime.strptime(date.strip(), r"%Y-%m-%d").date())
        if formattedDate not in self.dateMap:
            print("No Values for Requested Date")
            return 
        maxCount = 0
        activeCookies = []
        for key in self.dateMap[formattedDate].keys():
            if self.dateMap[formattedDate][key]>maxCount:
                activeCookies = []
                maxCount = self.dateMap[formattedDate][key]
                activeCookies.append(key)
            elif self.dateMap[formattedDate][key]==maxCount:
                activeCookies.append(key)
        for each_cookie in activeCookies:
            print(each_cookie)

    def save_logs(self):
        logging.basicConfig(filename=f"logs/mostActiveCookieLogs_{datetime.now()}",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Retrieve most Active Cookie on given Date")
    parser.add_argument("filepath", default=None, help="Path to cookies log file")
    parser.add_argument("-d", default=None, dest="date", help="Date for the most active cookie")
    args = parser.parse_args()

    if not args.date or not args.filepath:
        parser.print_help()
        sys.exit()

    data = most_active_cookie()
    data.read_file(args.filepath)
    data.printMostActive(args.date)
    data.save_logs()

# ---------- Open Qs -----------
# what if we couldn't hold it in memory?
# do I need to save things in the hashmap or could i just filter by date first and then count? Cookies in the log file are sorted by timestamp
# is hashmap over-engineering? long code is hard to maintain. depend on how easy it is to access the log file
# separate date object for easy manipulation and future company changes?
# what if file somehwere has some blank lines? Maybe validating the log file formaat strictly beforehand is an option
# normalize the timestamps to the required timezone?

# ---------- To-Dos -------------
# add read me (manual) for the command line program (.md file)