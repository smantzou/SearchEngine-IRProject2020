import eel
from QueryProcessor import processQuery, feedBackQuery
from general import file_to_dict

# Initialise the static folder
eel.init("static")


# Method that transfer the query info to QueryProcessor then returns it to Front End
@eel.expose
def getQueryInfo(topKResults, query):
    topKDict, query_time = processQuery(topKResults, query.split(" "))
    titleDict = returnTitles(topKDict)
    eel.receiveResults(topKDict, titleDict, query_time)


# Method that transfers the feed back info to QueryProcessor then returns it to Front End
@eel.expose
def receiveFeedback(feedBackDict):
    urlFeedBack = dict()
    for feed in feedBackDict:
        urlFeedBack.update({feed['key']: feed['value']})
    newTopK, query_time = feedBackQuery(urlFeedBack, urlFeedBack.__len__())
    newTitle = returnTitles(newTopK)
    eel.receiveResults(newTopK, newTitle, query_time)


# Method that returns the title of given Urls
def returnTitles(urlDict):
    titleDict = file_to_dict('Crawler/titles.pkl')
    partialTitleDict = dict()
    for url in urlDict.keys():
        title = titleDict.get(urlDict.get(url))
        partialTitleDict.update({url: title})
    return partialTitleDict


# start the app in a non browser window
# eel.start("noodleHomePage.html", mode='chrome', size=(1800, 1000))


# start the app by starting the browser window with localhost://8080 as the starting page
eel.start('noodleHomePage.html', mode='chrome-app', port=8080,
          cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])
