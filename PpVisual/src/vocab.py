import logging
from collections import Counter
import os
import numpy as np
from nltk.tokenize import word_tokenize
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class Vocab():
    def __init__(self, file):
        self.min_count = 1

        self.pad = 0
        self.unk = 1
        self._id2word = ['<pad>', '<unk>']
        self.word_count_1 = []
        self._id2extword = ['<pad>', '<unk>']

        self._id2label = []
        self.label_weights = []

        # self._id2label = ['Policy_Introductory', 'First_Party_Collection_and_Use', 'Cookies_and_Similar_Technologies', 'Third_Party_Share_and_Collection',
        #        'User_Right_and_Control','Data_Security', 'Data_Retention', 'International_Data_Transfer', 'Specific_Audiences',
        #        'Policy_Change', 'Policy_Contact_Information']
        #
        # self._id2label = list(map(lambda x: x.strip().lower(), self._id2label))

        self.build_vocab(file)

        reverse = lambda x: dict(zip(x, range(len(x))))
        self._word2id = reverse(self._id2word)
        self._label2id = reverse(self._id2label)
        self.id2label = self._id2label
        logging.info(str(self._id2label))
        logging.info("Build vocab: words %d, labels %d." % (self.word_size, self.label_size))

    def build_vocab(self, file):
        word_counter = Counter()
        label_counter = Counter()

        label_flag = True
        f = open(DIR+file, 'r', encoding='UTF-8', errors='ignore')
        lines = f.readlines()
        lines = list(map(lambda x: x.strip().lower(), lines))
        for line in lines:
            if line == '':
                label_counter[label] += 1
                label_flag = True
            else:
                if label_flag:
                    label = line
                    label_flag = False
                else:
                    words = word_tokenize(line)
                    for word in words:
                        word_counter[word] += 1

        for word, count in word_counter.most_common():
            if count >= self.min_count:
                self._id2word.append(word)
            if count == 1:
                self.word_count_1.append(word)

        for label, count in label_counter.most_common():
            self._id2label.append(label)
            self.label_weights.append(count)

    def load_pretrained_embs(self, embfile):
        with open(DIR+embfile, encoding='utf-8') as f:
            lines = f.readlines()[1:]
            word_count = len(lines)
            values = lines[0].split()
            embedding_dim = len(values) - 1

        index = len(self._id2extword)
        embeddings = np.zeros((word_count + index, embedding_dim))
        with open(DIR+embfile, encoding='utf-8') as f:
            for line in f.readlines()[1:]:
                values = line.split()
                self._id2extword.append(values[0])
                vector = np.array(values[1:], dtype='float64')
                try:
                    embeddings[self.unk] += vector
                    embeddings[index] = vector
                    index += 1
                except:
                    pass

        embeddings[self.unk] = embeddings[self.unk] / word_count
        embeddings = embeddings / np.std(embeddings)

        reverse = lambda x: dict(zip(x, range(len(x))))
        self._extword2id = reverse(self._id2extword)

        assert len(set(self._id2extword)) == len(self._id2extword)

        logging.info("Load extword embed: words %d, dims %d." % (self.extword_size, embedding_dim))

        return embeddings

    def word2id(self, xs):
        if isinstance(xs, list):
            return [self._word2id.get(x, self.unk) for x in xs]
        return self._word2id.get(xs, self.unk)

    def extword2id(self, xs):
        if isinstance(xs, list):
            return [self._extword2id.get(x, self.unk) for x in xs]
        return self._extword2id.get(xs, self.unk)

    def label2id(self, xs):
        if isinstance(xs, list):
            return [self._label2id.get(x, self.unk) for x in xs]
        return self._label2id.get(xs, self.unk)

    @property
    def word_size(self):
        return len(self._id2word)

    @property
    def extword_size(self):
        return len(self._id2extword)

    @property
    def label_size(self):
        return len(self._id2label)
