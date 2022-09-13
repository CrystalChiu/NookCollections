from ipaddress import ip_address
from pickle import FALSE, TRUE
from flask import Flask, render_template, request_started, url_for, jsonify, request
import requests
from requests import get
import re
from datetime import datetime

#NOTE: add unit tests to below function

# expecting input in the form "11 - 3" as given from ACNH API
# Returns list of bools with TRUE in available months
# Returns list of TRUE if available around the year
def toArray_months(monthRange):
    
    months = list()

    regex = r"(\d+)-(\d+)"
    result = re.search(regex, monthRange)

    if(result != None):
        for i in range(12):
            months.append(FALSE)

        start = int(result.group(1)) # start month (1-12)
        end = int(result.group(2)) # end month (1-12)

        # find number of months btwn start & end (1 if same month)
        numIterations = 0
        if(end >= start):
            numIterations = end - start
        else:
            numIterations = (end + 12) - start
        numIterations += 1

        # adding each month number to included months array
        monthNum = start

        while numIterations != 0:
            if(monthNum <= 12):
                months[monthNum - 1] = TRUE
            else:
                months[monthNum - 13] = TRUE

            monthNum += 1
            numIterations -= 1
    else:
        for i in range(12):
            months.append(TRUE)

    return months

# Takes string from API in the form "11am - 3pm"
# Returns list of bools with TRUE in available times
# Returns list of TRUE if available around the clock
def toArray_times(timeRange):
    times = list()
    regex = r"(\d+)(\w\w)\s-\s(\d+)(\w\w)"
    result = re.search(regex, timeRange)

    if(result != None):
        for i in range(24):
            times.append(FALSE)

        start_time = int(result.group(1))
        start_meridiem = str(result.group(2))
        end_time = int(result.group(3))
        end_meridiem = str(result.group(4))

        if(start_meridiem == "pm"):
            start_time += 12
        if(end_meridiem == "pm"):
            end_time += 12

        for i in range ((end_time - start_time) + 1):
            times[start_time + i] = TRUE
    else:
        for i in range(24):
            times.append(TRUE)

    return times

# Checks if each critter has availability in the current month/time
# If both are true - add to available critters list
# Returns list of avalailable critter names as string
def availableCritter(critterType, numCritters):
    availableCritters = list()
    curTime = datetime.now().hour
    curMonth = datetime.now().month

    numCritters += 1
    for id in range(1, numCritters, 1):
        correctMonth = FALSE
        correctTime = FALSE

        critter_id = str(id)
        response = requests.get(f'https://acnhapi.com/v1/{critterType}/{critter_id}')

        availableMonths = toArray_months(response.json()['availability']['month-northern'])
        availableTimes = toArray_times(response.json()['availability']['time'])

        #if current month is in included months ...
        if(availableMonths[curMonth - 1] == TRUE):
            correctMonth = TRUE

        #if current time is in included times ...
        if(availableTimes[curTime] == TRUE):
            correctTime = TRUE

        if(correctMonth == TRUE and correctTime == TRUE):
            critter = response.json()['file-name']
            availableCritters.append(critter)
        
    return availableCritters

app = Flask(__name__)
#make a new page for index
@app.route("/")
def index():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    availableFish = availableCritter("fish", 80)
    numFish = len(availableFish)

    availableSea = availableCritter("sea", 40)
    numSea = len(availableSea)

    availableBugs = availableCritter("bugs", 80)
    numBugs = len(availableBugs)

    # once we have our completed array of critters, return to jinja template
    return render_template('index.html', availibleFish = availableFish, numFish = numFish, availableSea = availableSea, 
                            numSea = numSea, availableBugs = availableBugs, numBugs = numBugs)

@app.route('/fish/<fish_id>')
def fish(fish_id):
    response = requests.get(f"https://acnhapi.com/v1/fish/{fish_id}/")
    fish_name = response.json()['file-name']

    # we need a loop that returns all fish to render template

    return render_template('index.html', fish_name = fish_name) 
    #left = name of new variable in jinja template; right = value we assign to new var
    #common convention -> name them the same thing

if __name__ == '__main__':
    app.run()




