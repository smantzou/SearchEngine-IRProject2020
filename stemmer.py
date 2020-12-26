import string
from nltk.corpus import stopwords
from general import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from indexer import makeUrlDict


def stemSentence(sentence):
    token_words = word_tokenize(sentence)
    token_words = [i for i in token_words if not i in stop_words]
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(porter.stem(word))
    return stem_sentence


porter = PorterStemmer()
newdict = file_to_dict('Crawler/dictionary.pkl')
for i in range(1):
    text = newdict[i].return_list()
    url = newdict[i].return_url()
    print(text)
    string_text = ' '.join(text)
    string_text = string_text.lower()
    string_text = string_text.translate(string_text.maketrans('', '', string.punctuation))
    string_text = string_text.strip()
    stop_words = set(stopwords.words('english'))
    makeUrlDict(url, stemSentence(string_text))