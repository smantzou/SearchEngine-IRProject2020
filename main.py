import eel
from QueryProcessor import processQuery

eel.init("static")


@eel.expose
def getQueryInfo(topKResults, query):
    topKDict = processQuery(topKResults, query.split(" "))
    print(topKDict)
    eel.receiveResults(topKDict)


@eel.expose
def receiveFeedback(feedbackArray):
    print(feedbackArray)


# start the app in a non browser window
# eel.start("noodleHomePage.html", mode='chrome', size=(1800, 1000))


# start the app by starting the browser window with localhost://8080 as the starting page
eel.start('noodleHomePage.html', mode='chrome-app', port=8080,
          cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])
