import pickle
import random
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BasicTokenizer

from src.vocab import Vocab

basic_tokenizer = BasicTokenizer()

# set seed
random.seed(666)
np.random.seed(666)


def convert_data2tfidf(files, vocab):
    for filename in files:
        file = open('./data/' + filename + '.data.pickle', 'rb')
        data = pickle.load(file)

        texts = data['text']
        if filename.startswith("train"):
            vectorizer = TfidfVectorizer(vocabulary=vocab._word2id)
            arrays = vectorizer.fit_transform(texts).toarray()
        else:
            arrays = vectorizer.transform(texts).toarray()

        dic = {'text': arrays, 'label': data['label']}
        file = open('./data/' + filename + '.tfidf.pickle', 'wb')
        pickle.dump(dic, file)
        file.close()

        print(filename, arrays.shape)


def convert_data(filename, vocab, max_sent_len=128):
    file = open('./data/' + filename + '.pickle', 'rb')
    data = pickle.load(file)

    examples = []
    labels = []
    for text, label in zip(data['review'], data['label']):
        words = basic_tokenizer.tokenize(text)
        words = [word if word in vocab._id2word else '<unk>' for word in words]
        sent_len = min(max_sent_len, len(words))
        assert sent_len > 0
        words = words[: max_sent_len]
        examples.append(' '.join(words))
        labels.append(label)

    dic = {'text': examples, 'label': labels}
    file = open('./data/' + filename + '.data.pickle', 'wb')
    pickle.dump(dic, file)
    file.close()
    print(filename, len(examples))


def convert_csv2data():
    def write_data(file_name, data):
        file = open(file_name, 'wb')
        pickle.dump(data, file)
        file.close()
        print(file_name, len(data['review']))

    lens = []
    for fold in range(10):
        # test
        f_test = pd.read_csv('./data/fold' + str(fold) + '.tsv', sep='\t', encoding='UTF-8')
        texts = f_test['review'].map(lambda x: x.lower()).tolist()
        labels = f_test['sentiment'].tolist()
        test_data = {'label': labels, 'review': texts}

        file_name = './data/test_' + str(fold) + '.pickle'
        write_data(file_name, test_data)

        # dev
        fold_ = (fold + 1) % 10
        f_dev = pd.read_csv('./data/fold' + str(fold_) + '.tsv', sep='\t', encoding='UTF-8')
        texts = f_dev['review'].map(lambda x: x.lower()).tolist()
        labels = f_dev['sentiment'].tolist()
        dev_data = {'label': labels, 'review': texts}

        file_name = './data/dev_' + str(fold) + '.pickle'
        write_data(file_name, dev_data)

        # train
        train_texts = []
        train_labels = []
        folds = []
        for i in range(2, 10):
            fold_ = (fold + i) % 10
            folds.append(fold_)
            f_train = pd.read_csv('./data/fold' + str(fold_) + '.tsv', sep='\t', encoding='UTF-8')
            train_texts.extend(f_train['review'].map(lambda x: x.lower()).tolist())
            train_labels.extend(f_train['sentiment'].tolist())
        print(folds)
        train_data = {'label': train_labels, 'review': train_texts}
        train_name = './data/train_' + str(fold) + '.pickle'
        write_data(train_name, train_data)

        lens.append(str([fold, len(train_data['review']), len(dev_data['review']), len(test_data['review'])])[1:-1])

    for fold in range(10):
        print(lens[fold])


if __name__ == "__main__":
    # convert_csv2data
    convert_csv2data()

    # convert_data
    for fold in range(10):
        cache_name = "./res/vocab_" + str(fold) + ".pickle"
        train = "train_" + str(fold)
        dev = "dev_" + str(fold)
        test = "test_" + str(fold)
        files = [train, dev, test]

        # biuld vocab
        if Path(cache_name).exists():
            vocab_file = open(cache_name, 'rb')
            vocab = pickle.load(vocab_file)
            print('load vocab from ' + cache_name)
        else:
            vocab = Vocab('./data/' + train + '.pickle')
            file = open(cache_name, 'wb')
            pickle.dump(vocab, file)
            print('res vocab to ' + cache_name)

        # review2data
        for file in files:
            convert_data(file, vocab)

        # data2tfidf
        convert_data2tfidf(files, vocab)
