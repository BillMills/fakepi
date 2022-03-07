import random, datetime, math
from flask import Flask, request

app = Flask(__name__)

def fakeHumidity(minofday):
    minute = (minofday - 300)%1440
    low = 65
    high = 90
    jitter = 3
    highperiod = [630, 810] # 10:30 to 1:30 in minutes of the day
    onset = max(highperiod[0] - 300, 0)
    offset = min(highperiod[1] + 300,1440)

    if minute <= onset:
        return low + (random.random()-1)*jitter
    elif onset < minute <= highperiod[0]:
        return low + (high-low)/(highperiod[0] - onset) * (minute - onset) + (random.random()-1)*jitter
    elif highperiod[0] < minute <= highperiod[1]:
        return high + (random.random()-1)*jitter
    elif highperiod[1] < minute < offset:
        return high + (low-high)/(offset - highperiod[1]) * (minute - highperiod[1] ) + (random.random()-1)*jitter
    else:
        return low + (random.random()-1)*jitter

def fakeTemperature(minofday):
    minute = (minofday - 300)%1440
    period = 1440
    hottest = 780
    average = 50
    amplitude = 10

    return average + amplitude*math.cos( (minute - hottest)*2*math.pi/period )

start = datetime.datetime.now()

humidity = []
temperature = []
for i in range(1440):
    ts = start - datetime.timedelta(minutes=1440-i)
    point = {
        "val": fakeHumidity(ts.hour*60 + ts.minute),
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
    }
    humidity.append(point)

    point = {
        "val": fakeTemperature(ts.hour*60 + ts.minute),
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")   
    }
    temperature.append(point)


@app.route("/greenhouse")
def hello_world():
    if 'humidity' in request.args:
        return {"humidity": humidity}
    elif 'temperature' in request.args:
        return {"temperature": temperature}
    else:
        return "Unrecognized query string parameter; should be ?humidity or ?temperature"

@app.route("/update")
def up():
    humidity.pop(0)
    temperature.pop(0)
    ts = datetime.datetime.now()
    humidity.append({
        "val": fakeHumidity(ts.hour*60 + ts.minute),
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")   
    })
    temperature.append({
        "val": fakeTemperature(ts.hour*60 + ts.minute),
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")   
    })

    return "OK"
