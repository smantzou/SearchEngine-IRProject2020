from general import *


adict = file_to_dict('Indexer/countDict.pkl')
cdict = file_to_dict('Indexer/freq_dictionary.pkl')
inverted = file_to_dict('Indexer/invertedIndex.pkl')
counter = dict()
for keys in inverted.keys():
    for url in inverted.get(keys):
        if url not in counter.keys():
            counter.update({url: 1})
print(counter.__len__())

print(adict.__len__())
print(cdict.__len__())
from general import file_to_dict
#
# crawlDict = file_to_dict('Crawler/dictionary.pkl')
# print(list(crawlDict.keys())[-1])
# for key in crawlDict.keys():
#     print(crawlDict.get(key).return_url())
#     if crawlDict.get(key).return_url() == 'https://www.python.org/ftp/python/3.3.2/python332.chm':
#         print('gamoto')
# from urllib.request import urlopen
#
# response = urlopen('https://www.python.org/users/membership/')
# print(response.getheader('Content-Type'))
# try:
#     if response.getheader('Content-Type').split(';')[0] == 'text/html':
#         print('yes')
# except Exception as ex:
#     print(ex)
#     print('Error : can not crawled page ')
