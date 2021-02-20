import eel
from QueryProcessor import processQuery
from general import file_to_dict

eel.init("static")


@eel.expose
def getQueryInfo(topKResults, query):
    topKDict = processQuery(topKResults, query.split(" "))
    titleDict = returnTitles(topKDict)
    eel.receiveResults(topKDict, titleDict)


@eel.expose
def receiveFeedback(feedBackDict):
    urlFeedBack = dict()
    for feed in feedBackDict:
        urlFeedBack.update({feed['key']: feed['value']})
    print(urlFeedBack)


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
