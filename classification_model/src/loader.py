import logging
import pickle
from collections import Counter
from pathlib import Path

import numpy as np
from transformers import BasicTokenizer

basic_tokenizer = BasicTokenizer()

from module import *


def get_examples(file_name, word_encoder, vocab, max_sent_len=128):
    mode = file_name.split('/')[-1][:-12]  # train validation test

    if isinstance(word_encoder, WordBertEncoder):
        cache_name = './data/' + mode + '.bert.pickle'
    else:
        cache_name = './data/' + mode + '.lstm.pickle'

    if Path(cache_name).exists():
        file = open(cache_name, 'rb')
        examples = pickle.load(file)
        logging.info('Data from cache file: %s, total %d docs.' % (cache_name, len(examples)))
        return examples

    label2id = vocab.label2id
    examples = []

    file = open(file_name, 'rb')
    data = pickle.load(file)

    len_counter = Counter()

    for text, label in zip(data['text'], data['label']):
        # label
        id = label2id(label)
        if isinstance(word_encoder, WordEncoder):
            # words
            words = basic_tokenizer.tokenize(text)
            len_counter[len(words)] += 1
            sent_len = len(words)

            word_ids = vocab.word2id(words)
            extword_ids = vocab.extword2id(words)

            examples.append([id, sent_len, word_ids, extword_ids])

        elif isinstance(word_encoder, WordBertEncoder):
            bert_indices, basic_ids = word_encoder.bert2basic(text,
                                                              max_sent_len)  # list: bert_token_id, basic_token_id align

            bert_len, basic_len = len(bert_indices), len(basic_ids)
            len_counter[bert_len] += 1

            assert bert_len > 0

            examples.append([id, (bert_len, basic_len), bert_indices, basic_ids])

    logging.info('Data from file: %s, total %d docs.' % (file_name, len(examples)))

    # for length, count in len_counter.most_common():
    #     print(length, count)

    file = open(cache_name, 'wb')
    pickle.dump(examples, file)
    logging.info('Cache Data to file: %s, total %d docs.' % (cache_name, len(examples)))
    return examples


def batch_slice(data, batch_size):
    batch_num = int(np.ceil(len(data) / float(batch_size)))
    for i in range(batch_num):
        cur_batch_size = batch_size if i < batch_num - 1 else len(data) - batch_size * i
        docs = [data[i * batch_size + b] for b in range(cur_batch_size)]

        yield docs


def data_iter(data, batch_size, shuffle=True):
    """
    randomly permute data, then sort by source length, and partition into batches
    ensure that the length of  sentences in each batch
    """

    batched_data = []
    if shuffle:
        np.random.shuffle(data)

    batched_data.extend(list(batch_slice(data, batch_size)))

    if shuffle:
        np.random.shuffle(batched_data)

    for batch in batched_data:
        yield batch
