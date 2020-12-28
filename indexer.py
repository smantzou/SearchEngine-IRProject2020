from stemmer import stemDictionary, return_UrlDict
from general import *

index_dict = file_to_dict('Index/tempIndex.pkl')


# na thn kaloyme apo eksw
# na ftiaksoyme mia methodo poy tha fortwnei to tempindex
# mia methodo poy tha kanei index mexri oso ths poyme
# mia methodo poy tha kaleitai otan exoyme ftasei ena sygkekrimeno arithmo megethoys sto temp index
# mia methodo poy tha kanei update ton megalo index
# na diorthwsoyme bugs toy stemmer
# na mhn mpainei o crawler se oti rossoblyat selida briskei aka ban DOMAINS
# ean den mporei na mpei sthn prwth selida poy toy dinetai na pairnei mia allh
# ena main script san toy crawler gia na diaxeirizetai ton indexer kai na dexetai kai orismata
def initIndexProcess():
    stemDictionary()
    url_dict = return_UrlDict()
    startIndex(url_dict, 'Index/tempIndex.pkl')
    # else:
    #     print('Updating...')
    #     updateIndex(url_dict, 'Index/tempIndex.pkl')


def startIndex(url_dict, file):
    for urlkey in url_dict.keys():
        word_dict = url_dict.get(urlkey)
        for wordkey in word_dict.keys():
            if wordkey in index_dict.keys():
                index_dict.get(wordkey).update({urlkey: word_dict.get(wordkey)})
            else:
                index_dict.update({wordkey: {}})
                v = {urlkey: word_dict.get(wordkey)}
                index_dict[wordkey] = v

    dict_to_file(index_dict, file)
    printIndex()


# def updateIndex(url_dict, file):
#     for urlkey in url_dict.keys():
#         for wordkey in url_dict.get(urlkey).keys():
#
#             if wordkey in index_dict.keys():
#                 if urlkey in index_dict.get(wordkey).keys():
#                     if index_dict.get(wordkey).get(urlkey) == url_dict.get(urlkey).get(wordkey):
#                         continue
#                     else:
#                         index_dict.get(wordkey).update({urlkey: url_dict.get(urlkey).get(wordkey)})
#                 else:
#                     index_dict.get(wordkey).update({urlkey: url_dict.get(urlkey).get(wordkey)})
#             else:
#                 index_dict.update({wordkey, index_dict.get(wordkey).update({urlkey: url_dict.get(urlkey).get(wordkey)})})
#
#     dict_to_file(index_dict, file)


def printIndex():
    for key in index_dict:
        print(key + '-->' + str(index_dict.get(key)))


initIndexProcess()
