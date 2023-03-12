#from pickle import FALSE, TRUE
from pickle import FALSE, TRUE
from flask import Flask, render_template, request_started, url_for, jsonify, request, send_file
import requests
#from requests import get
import re
from datetime import datetime

#<------------------Supplemental Functions------------------>

app = Flask(__name__)

# O(1) time, O(1) space
def validTime(timeRange, curTime):
    if(curTime in timeRange): return True
    return False

# O(n) time, O(1) space
#takes in the current month and the months the critter is available
#outputs whether or not the current month falls within available range (true) or not (false)
def validMonth(monthRange, curMonth):
    if(curMonth in monthRange): return True
    return False

# O(n) time
def availCritters(critterType, numCritters):
    curTime = datetime.now().hour
    curMonth = datetime.now().month
    result = list()

    for id in range(1, numCritters + 1, 1):
        critterId = str(id)
        response = requests.get(f'https://acnhapi.com/v1/{critterType}/{critterId}')

        month = validMonth(response.json()['availability']['month-array-northern'], curMonth)
        time = validTime(response.json()['availability']['time-array'], curTime)

        if(month and time):
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
    availBugs = availCritters("bugs", BUGNUM)
    availSea = availCritters("sea", SEANUM)

    return render_template('index.html', availFish = availFish, availBugs = availBugs, availSea = availSea)

if __name__ == '__main__':
    app.run()

#need to clear up space and run: xcode-select --install

