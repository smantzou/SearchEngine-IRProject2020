import string
from nltk.corpus import stopwords
from general import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from num2words import num2words


def stemPage(page, stopWords):
    """This function is responsible for stemming every token that we have received from a page,
    returns a list with stemmed words, no stopwords, numbers has been converted to words """

    porter = PorterStemmer()
    text = page[1]
    url = page[0]
    string_text = ' '.join(text)
    string_text = string_text.lower()
    string_text = string_text.translate(string_text.maketrans('', '', string.punctuation))
    string_text = string_text.strip()
    token_words = word_tokenize(string_text)
    token_words = [i for i in token_words if not i in stopWords]
    stemSentence = []
    for word in token_words:
        if word.isdigit():
            if word.__len__() > 5:
                continue
            if isDecimal(word):
                continue
            word = num2words(word)
        else:
            if not isEnglish(word):
                continue
        stemSentence.append(porter.stem(word))
    # return an empty dictionary if no words exist in page
    if stemSentence.__len__() == 0:
        print(url, " has no words")
        return dict()
    return makeUrlDict(url, stemSentence)


def makeUrlDict(url, stemSentence):
    """This function create and returns a word dictionary, from words to number of appearances """

    word_dict = dict()
    """Here we create the word dictionary with values number of appearances """
    for stemmedToken in stemSentence:
        if stemmedToken not in word_dict.keys():
            word_dict.update({stemmedToken: 1})
        else:
            num_of_app = word_dict.get(stemmedToken)
            word_dict.pop(stemmedToken)
            num_of_app += 1
            word_dict.update({stemmedToken: num_of_app})
    v = word_dict
    return v




def isDecimal(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def stemQuery(query):
    """The query first pass from here """
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
