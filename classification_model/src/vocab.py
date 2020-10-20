import logging
import pickle
from collections import Counter

import numpy as np
from transformers import BasicTokenizer

basic_tokenizer = BasicTokenizer()

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class Vocab():
    def __init__(self, file):
        self.min_count = 2
        self.max_len = 128

        self.pad = 0
        self.unk = 1
        self._id2word = ['<pad>', '<unk>']
        self._id2extword = ['<pad>', '<unk>']

        self._id2label = []
        self.target_names = []
        self.label_weights = []

        self.build_vocab(file)

        reverse = lambda x: dict(zip(x, range(len(x))))
        self._word2id = reverse(self._id2word)
        self._label2id = reverse(self._id2label)

        logging.info("Build vocab: words %d, labels %d." % (self.word_size, self.label_size))

    def build_vocab(self, file):
        file = open(file, 'rb')
        data = pickle.load(file)

        self.word_counter = Counter()

        for text in data['review']:
            words = basic_tokenizer.tokenize(text)
            for word in words:
                self.word_counter[word] += 1

        for word, count in self.word_counter.most_common():
            if count >= self.min_count:
                self._id2word.append(word)

        label2name = {0: 'Other',
                      1: 'Collect_Personal_Information',
                      2: 'Data_Retention_Period',
                      3: 'Data_Processing_Purposes',
                      4: 'Controller_Contact_Details',
                      5: 'Rights_of_Accessing',
                      6: 'Rights_of_Tectification_or_Erasure',
                      7: 'Rights_of_Restricting_Processing',
                      8: 'Rights_of_Object_to_Processing',
                      9: 'Rights_of_Data_Portability',
                      10: 'Lodge_a_Complaint'}

        self.label_counter = Counter(data['label'])

        for label in range(len(self.label_counter)):
            count = self.label_counter[label]
            self._id2label.append(label)
            self.target_names.append(label2name[label])
            self.label_weights.append(count)

    def load_pretrained_embs(self, embfile):
        with open(embfile, encoding='utf-8') as f:
            lines = f.readlines()
            word_count = len(lines)
            values = lines[0].split()
            embedding_dim = len(values) - 1

        index = len(self._id2extword)
        embeddings = np.zeros((word_count + index, embedding_dim))
        with open(embfile, encoding='utf-8') as f:
            for line in f.readlines():
                values = line.split()
                self._id2extword.append(values[0])
                vector = np.array(values[1:], dtype='float64')
                embeddings[self.unk] += vector
                embeddings[index] = vector
                index += 1

        embeddings[self.unk] = embeddings[self.unk] / word_count
        embeddings = embeddings / np.std(embeddings)

        reverse = lambda x: dict(zip(x, range(len(x))))
        self._extword2id = reverse(self._id2extword)

        assert len(set(self._id2extword)) == len(self._id2extword)

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
