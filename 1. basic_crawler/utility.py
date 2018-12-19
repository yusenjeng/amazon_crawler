import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def normalizeUrl(url):
    idx = url.find('url=')
    url = url[idx+4:]
    url = url.replace('%3A', ':')
    url = url.replace('%2F', '/')
    idx = url.find('ref')
    return url[:idx]


def cleanedTokenize(sentence):
    stops = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    words = word_tokenize(sentence.lower())
    tokens = [w for w in words if not w in stops]
    tokens = [t for t in tokens if t.isalpha() or t.isnumeric()]
    tokens_lemmatized = [lemmatizer.lemmatize(t) for t in tokens]

    # print('==============')
    # print(sentence)
    # print('=>', tokens)
    # print('=>', tokens_lemmatized)

    return tokens_lemmatized


def hasAsin(tag):
    return tag.has_attr('data-asin')


class Log():
    def __init__(self, fn='log.txt', mode='a'):
        self.fn = fn
        self.f = open(fn, mode)

    def write(self, tag, msg):
        self.f.write('['+tag+'] ' + msg + '\n')

    def close(self):
        if self.f:
            self.f.close()


class LogJSON():
    def __init__(self, fn='log.txt', mode='a'):
        self.fn = fn
        self.f = open(fn, mode)

    def write(self, msg):
        s = json.dumps(msg)
        self.f.write(s)
        self.f.write('\n')

    def close(self):
        if self.f:
            self.f.close()


class CrawlerError(Exception):
    def __init__(self, msg, code=1):
        self.code = code
        self.msg = msg
