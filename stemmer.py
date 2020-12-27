import string
from nltk.corpus import stopwords
from general import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from num2words import num2words

word_dict = dict()
url_dict = dict()


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

        stem_sentence.append(porter.stem(word))
    return stem_sentence


def stemDictionary():
    crawldict = file_to_dict('Crawler/dictionary.pkl')
    for i in range(crawldict.__len__()):
        text = crawldict[i].return_list()
        url = crawldict[i].return_url()
        string_text = ' '.join(text)
        string_text = string_text.lower()
        string_text = string_text.translate(string_text.maketrans('', '', string.punctuation))
        string_text = string_text.strip()
        makeUrlDict(url, stemSentence(string_text))

    crawldict.clear()
    dict_to_file(crawldict, 'Crawler/dictionary.pkl')


def makeUrlDict(url, stemmedTokens):
    for stemmedToken in stemmedTokens:
        if stemmedToken not in word_dict.keys():
            word_dict.update({stemmedToken: 1})
        else:
            num_of_app = word_dict.get(stemmedToken)
            word_dict.pop(stemmedToken)
            num_of_app += 1
            word_dict.update({stemmedToken: num_of_app})
    url_dict.update({url: word_dict})
    word_dict.clear()


def return_UrlDict():
    return url_dict
