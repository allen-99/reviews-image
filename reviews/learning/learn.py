import string
import warnings

import joblib
import numpy as np
import pandas as pd
import pymorphy2
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from reviews.models.models import Text, Model

pretext = ['в', 'на', 'о', 'с', 'у', 'к', 'по', 'за', 'из', 'от', 'до', 'перед', 'через', 'среди', 'между', 'вокруг',
           'около', 'возле', 'над', 'под', 'внизу', 'вверху', 'вглубь', 'вдоль', 'насчет', 'со', 'путем']
unions = ['а', 'и', 'но', 'или', 'да', 'как', 'так', 'чем', 'ли', 'же', 'только', 'хоть', 'раз', 'даже', 'после',
          'пока', 'тогда', 'хотя', 'если', 'поскольку', 'потому', 'ибо', 'оттого', 'затем', 'ведь', 'чтобы', 'чтоб',
          'словно', 'будто', 'точно', 'когда', 'как только', 'также', 'таким образом', 'следовательно', 'в результате',
          'итак', 'дабы']

stop_words = unions + pretext


def create_bag_of_words(text):
    filtered_doc = []
    morph = pymorphy2.MorphAnalyzer()

    doc = word_tokenize(text, language='russian')
    tokens = [word.lower() for word in doc if word not in string.punctuation]
    filtered_words = [word for word in tokens if word.lower() not in stop_words]
    lemma_words = []
    for word in filtered_words:
        parses = morph.parse(word)
        lemma = parses[0].normal_form
        lemma_words.append(lemma)
    filtered_doc.append(filtered_words)
    bigrams = ngrams(lemma_words, 2)
    trigrams = ngrams(lemma_words, 3)

    bag_of_words = {}
    for token in lemma_words:
        bag_of_words[token] = bag_of_words.get(token, 0) + 1
    for bigram in bigrams:
        token = ' '.join(bigram)
        bag_of_words[token] = bag_of_words.get(token, 0) + 1

    return bag_of_words


class Learn:

    def learn(self, name, algorithm, set_of_text):
        warnings.filterwarnings('ignore')
        reviews = Text.objects.filter(set=set_of_text)
        data = pd.DataFrame(reviews.values('text', 'rating', 'date'))
        vectorizer = TfidfVectorizer(analyzer=create_bag_of_words)
        texts = data['text']
        labels = data['rating']

        X = vectorizer.fit_transform(texts)
        y = labels.to_numpy()

        if algorithm == 'svm':

            param_grid_kernel = [
                {'kernel': ['linear'], 'C': np.arange(0.1, 1, 0.1)},
                {'kernel': ['poly'], 'degree': [2, 3, 4], 'C': np.arange(0.1, 1, 0.1)},
                {'kernel': ['rbf'], 'gamma': [0.0001, 0.001, 0.01, 1, 5, 10], 'C': np.arange(0.1, 1, 0.1)},
                {'kernel': ['sigmoid'], 'gamma': [0.0001, 0.001, 0.01, 1, 5, 10], 'C': np.arange(0.1, 1, 0.1)}
            ]

            kf = KFold(n_splits=20, shuffle=True)
            grid_search_kernel = GridSearchCV(SVC(), param_grid=param_grid_kernel, cv=kf)
            svc_params_result = grid_search_kernel.best_params_
            grid_search_kernel.fit(X, y)
            model = Model()
            model.name = name
            model.type = algorithm
            model.parameters = svc_params_result
            joblib.dump(grid_search_kernel, f"models/{name}.pkl")
            joblib.dump(vectorizer, f"models/vect/{name}.pkl")
            model.model_data.name = f"models/{name}.pkl"
            model.vectorizer.name = f"models/vect/{name}.pkl"
            with open(f"models/{name}.pkl", 'rb') as f:
                model.model_data.save("models/{name}.pkl", f, save=True)
            with open(f"models/vect/{name}.pkl", 'rb') as f:
                model.vectorizer.save("models/vect/{name}.pkl", f, save=True)
            model.save()
        else:
            counts = data['rating'].value_counts()
            counts = counts.sort_index()
            count_pre = [(count / len(data['rating']) * 100) for count in counts]
            count_pre_reverse = [(1 / count * 100) for count in count_pre]

            params = {
                'alpha': np.arange(0, 1.1, 0.1),
                'fit_prior': [True, False],
                'class_prior': [None, count_pre, count_pre_reverse],
            }

            kf = KFold(n_splits=20, shuffle=True)
            grid_bayes = GridSearchCV(MultinomialNB(), params, cv=kf)
            grid_bayes.fit(X, y)

            svc_params_result = grid_bayes.best_params_
            model = Model()
            model.name = name
            model.type = algorithm
            model.parameters = svc_params_result
            joblib.dump(grid_bayes, f"models/{name}.pkl")
            joblib.dump(vectorizer, f"models/vect/{name}.pkl")
            data = joblib.load(f"models/{name}.pkl")
            vect = joblib.load(f"models/vect/{name}.pkl")
            model.vectorizer.path(f"models/vect/{name}.pkl")
            model.model_data.save(f"models/{name}.pkl", data, save=True)
            model.save()
