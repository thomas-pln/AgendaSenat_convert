from ics import Calendar, Event
import os
from jsonConvert import convertToJSON

def convertToICS(json):

    c = Calendar()
    for act in json:
        e = Event()
        e.name = act.title
        e.begin = act.date+act.time

        c.events.add(e)

    print(c.events)

    return c



def saveICS(fileName, calendar):
    with open(fileName, 'w') as my_file:
        my_file.writelines(calendar)


def icsConvert(httpResponse ,date):
    jsonArr = convertToJSON(httpResponse, date)
    icsVar =  convertToICS(jsonArr)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    saveICS(dir_path+'/../data/agenda.ics', icsVar)