#from pickle import FALSE, TRUE
from flask import Flask, render_template, request_started, url_for, jsonify, request, send_file
import requests
#from requests import get
import re
from datetime import datetime

#<------------------Supplemental Functions------------------>

app = Flask(__name__)

# O(1) time, O(1) space
def validTime(timeRange, curTime):
    regex = r"(\d+)(\w\w)\s-\s(\d+)(\w\w)"
    result = re.search(regex, timeRange)

    # when None is returned, there is no time -> always available
    if(result == None):
        return True
    else:
        # store capture groups in int and string variables
        startTime = int(result.group(1))
        startMeridiem = str(result.group(2))
        endTime = int(result.group(3))
        endMeridiem = str(result.group(4))

        # adjust to military time
        start = startTime
        if(startMeridiem == 'pm'):
            start += 12
        end = endTime
        if(endMeridiem == 'pm'):
            end += 12

        # check if user's time is between start and end time
        if(curTime >= start and curTime <= end):
            return True
        return False

# O(n) time, O(1) space
def validMonth(monthRange, curMonth):
    regex = r"(\d+)-(\d+)"
    result = re.search(regex, monthRange)
    NUM_MONTHS = 12

    if(result == None):
        return True
    else:
        startMonth = int(result.group(1)) # start month (1-12)
        endMonth = int(result.group(2)) # end month (1-12)

        if(curMonth >= startMonth):
            if(curMonth >= startMonth and curMonth <= 12):
                return True
            elif (curMonth >= 1 and curMonth <= endMonth):
                return True
        else:
            if(curMonth >= startMonth and curMonth <= endMonth):
                return True

        return False

# O(n) time
def availCritters(critterType, numCritters):
    curTime = datetime.now().hour
    curMonth = datetime.now().month
    result = list()

    for id in range(1, numCritters, 1):
        critterId = str(id)
        response = requests.get(f'https://acnhapi.com/v1/{critterType}/{critterId}')
        availableMonths = response.json()['availability']['month-northern']
        availableTimes = response.json()['availability']['time']

        if(validMonth(availableMonths, curMonth) and validTime(availableTimes, curTime)):
            result.append(response.json()['file-name']) # this can be changed to support the graphics in index.html
        
        return result

#<------------------Flask------------------>

# O(1) time, O(n) space
@app.route("/")
def index():

    # find user's current time
    curTime = datetime.now().hour
    curMonth = datetime.now().month

    #set constants and create resultant lists
    availFish = list()
    FISHNUM = 80
    availBugs = list()
    BUGNUM = 80
    availSea = list()
    SEANUM = 30

    availFish = availCritters("fish", FISHNUM)
    availBugs = availCritters("bug", BUGNUM)
    availSea = availCritters("sea", SEANUM)

    return render_template('index.html', availFish, availBugs, availSea)

if __name__ == '__main__':
    app.run()

#need to clear up space and run: xcode-select --install

