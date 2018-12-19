import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class NLPParser():
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def normalizeUrl(self, url):
        idx = url.find('url=')
        url = url[idx+4:]
        url = url.replace('%3A', ':')
        url = url.replace('%2F', '/')
        idx = url.find('ref')
        return url[:idx]

    def understand(self, sentence):
        stops = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        words = word_tokenize(sentence.lower())
        tokens = [w for w in words if not w in stops]
        tokens = [t for t in tokens if t.isalpha() or t.isnumeric()]
        tokens_lemmatized = [lemmatizer.lemmatize(t) for t in tokens]

        # print('==============')
        # print('=>', tokens)
        # print('=>', tokens_lemmatized)

        return tokens_lemmatized


if __name__ == '__main__':
    parser = NLPParser()
    ret = parser.understand(
        'Gardein Ultimate Beefless Burger Meat Free Protein Packed Patties, Ready in 3 Minutes, 4 Pack (Frozen)')
    print(ret)
