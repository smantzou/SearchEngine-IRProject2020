import string
import numpy as np
from general import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from num2words import num2words

freq_dict = dict()
count_dict = dict()


def stebmPage(page, stopWords):
    porter = PorterStemmer()
    text = page[1]
    url = page[0]
    string_text = ' '.join(text)
    string_text = string_text.lower()
    string_text = string_text.translate(string_text.maketrans('', '', string.punctuation))
    string_text = string_text.strip()
    token_words = word_tokenize(string_text)
    token_words = [i for i in token_words if not i in stopWords]
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

    return makeUrlDict(url, stem_sentence)


def makeUrlDict(url, stemSentence):
    url_dict = dict()
    word_dict = dict()
    for stemmedToken in stemSentence:
        if stemmedToken not in word_dict.keys():
            word_dict.update({stemmedToken: 1})
        else:
            num_of_app = word_dict.get(stemmedToken)
            word_dict.pop(stemmedToken)
            num_of_app += 1
            word_dict.update({stemmedToken: num_of_app})
    array = np.array(list(word_dict.values()))
    count_dict.update({url: array})
    values = word_dict.values()
    if values.__len__() == 0:
        freq_dict.update({url: 0})
    else:
        maxF = max(values)
        freq_dict.update({url: maxF})
    url_dict.update({url: {}})
    v = word_dict
    url_dict[url] = v
    return url_dict


def return_freq():
    return freq_dict


def return_count_dict():
    return count_dict


# Need to send stop words as arguement
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
