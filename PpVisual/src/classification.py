from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
import csv
import re
import string
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
from preprocess import predict_precess
import pandas as pd


def get_SVM(file_data):
    a = file_data.split('\n')
    label = "pp_classification"
    classifier_linear = load("./model/pp_classification_svm.joblib")
    vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True, use_idf=True)
    label = "10_classification"

    classification_name = label.replace(" ", "_").replace("/", "_")
    train_path = "./dataset/" + classification_name + '_train_data.tsv'

    data_train = pd.read_csv(train_path, sep='\t')
    train_vectors = vectorizer.fit_transform(data_train.review)

    data_origin, data = predict_precess.predict_preprocess(file_data)
    data_test = pd.DataFrame(data, columns=['review'])
    test = vectorizer.transform(data_test.review)
    p = classifier_linear.predict(test)
    return p, data
