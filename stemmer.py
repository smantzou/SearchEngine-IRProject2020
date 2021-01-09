import string
from nltk.corpus import stopwords
from general import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from num2words import num2words
import os

url_dict = dict()
freq_dict = dict()


def stemSentence(sentence):
    porter = PorterStemmer()
    token_words = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    token_words = [i for i in token_words if not i in stop_words]
    stem_sentence = []
    for word in token_words:
        if word.isdigit():
            if word.__len__() > 5:
                continue
            word = num2words(word)
        else:
            if not isEnglish(word):
                continue

        stem_sentence.append(porter.stem(word))
    return stem_sentence


def stemDictionary(numberOfIndexes):
    crawlDict = file_to_dict('Crawler/dictionary.pkl')
    if crawlDict.__len__() == 0:
        print("Crawled Dictionary is empty...All crawled pages have been indexed ,please crawl some pages first! ")
        os._exit(0)
    if int(numberOfIndexes) > crawlDict.__len__():
        print("Requested number of indexes larger than crawled pages...Crawled Dictionary will be empty after run!")
        numberOfIndexes = crawlDict.__len__()
    for _ in range(0, int(numberOfIndexes)):
        crawlDictItem = crawlDict.popitem()
        aTextItem = crawlDictItem[1]
        text = aTextItem.return_list()
        url = aTextItem.return_url()
        string_text = ' '.join(text)
        string_text = string_text.lower()
        string_text = string_text.translate(string_text.maketrans('', '', string.punctuation))
        string_text = string_text.strip()
        makeUrlDict(url, stemSentence(string_text))

    dict_to_file(crawlDict, 'Crawler/dictionary.pkl')
def stemQuery():
    text = aTextItem.return_list()
    url = aTextItem.return_url()
    string_text = ' '.join(text)
    string_text = string_text.lower()
    string_text = string_text.translate(string_text.maketrans('', '', string.punctuation))
    string_text = string_text.strip()
    makeUrlDict(url, stemSentence(string_text))

def makeUrlDict(url, stemmedTokens):
    word_dict = dict()
    for stemmedToken in stemmedTokens:
        if stemmedToken not in word_dict.keys():
            word_dict.update({stemmedToken: 1})
        else:
            num_of_app = word_dict.get(stemmedToken)
            word_dict.pop(stemmedToken)
            num_of_app += 1
            word_dict.update({stemmedToken: num_of_app})

    values = word_dict.values()
    if values.__len__() == 0:
        freq_dict.update({url: 0})
    else:
        maxf = max(values)
        freq_dict.update({url: maxf})

    url_dict.update({url: {}})
    v = word_dict
    url_dict[url] = v


def return_freq():
    return freq_dict


def return_UrlDict():
    return url_dict


def stemQuery(query):
    porter = PorterStemmer()
    sentence = ' '.join(query)
    sentence = sentence.lower()
    sentence = sentence.translate(sentence.maketrans('', '', string.punctuation))
    sentence = sentence.strip()
    token_words = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    token_words = [i for i in token_words if not i in stop_words]
    stem_sentence = []
    for word in token_words:
        if word.isdigit():
            if word.__len__() > 5:
                continue
            word = num2words(word)
        else:
            if not isEnglish(word):
                continue

        stem_sentence.append(porter.stem(word))
    return stem_sentence
