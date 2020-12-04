import logging
import os
import numpy as np
import torch
from nltk.tokenize import word_tokenize
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from module.word_encoder import WordEncoder


def getExamples(file, word_encoder, vocab, max_doc_len=1, max_sent_len=128):
    label2id = vocab.label2id

    examples = []

    doc = []
    label_flag = True
    f = open(DIR+file, 'r', encoding='UTF-8')
    lines = f.readlines()
    lines = list(map(lambda x: x.strip().lower(), lines))
    for line in lines:
        if line == '':
            if len(doc) >= max_doc_len:
                examples.append([label2id(label), len(doc), doc])

            doc = []
            label_flag = True
        else:
            if label_flag:
                label = line
                label_flag = False
            else:
                if isinstance(word_encoder, WordEncoder):
                    words = word_tokenize(line)
                    sent_len = min(max_sent_len, len(words))
                    if sent_len == 0:
                        continue
                    words = words[: max_sent_len]
                    word_ids = vocab.word2id(words)
                    word_ids = torch.tensor(word_ids)
                    extword_ids = vocab.extword2id(words)
                    extword_ids = torch.tensor(extword_ids)
                    doc.append([sent_len, word_ids, extword_ids])
                else:
                    text = line.replace('##', '@@')
                    outputs = word_encoder.tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
                    bert_indices = outputs["input_ids"].squeeze()
                    segments_id = outputs["token_type_ids"].squeeze()
                    sent_len = min(max_sent_len, bert_indices.shape[0])
                    doc.append([sent_len, bert_indices[:max_sent_len], segments_id[:max_sent_len]])

    if len(doc) >= max_doc_len:
        examples.append([label2id(label), len(doc), doc])

    logging.info('Data from file: %s, total %d docs.' % (file, len(examples)))

    return examples


def getTestExamples(test_data, word_encoder, vocab, max_doc_len=1, max_sent_len=128):
    label2id = vocab.label2id

    examples = []

    doc = []
    label_flag = True

    lines = test_data
    lines = list(map(lambda x: x.strip().lower(), lines))
    for line in lines:
        if line == '':
            if len(doc) >= max_doc_len:
                examples.append([label2id(label), len(doc), doc])

            doc = []
            label_flag = True
        else:
            if label_flag:
                label = line
                label_flag = False
            else:
                if isinstance(word_encoder, WordEncoder):
                    words = word_tokenize(line)
                    sent_len = min(max_sent_len, len(words))
                    if sent_len == 0:
                        continue
                    words = words[: max_sent_len]
                    word_ids = vocab.word2id(words)
                    word_ids = torch.tensor(word_ids)
                    extword_ids = vocab.extword2id(words)
                    extword_ids = torch.tensor(extword_ids)
                    doc.append([sent_len, word_ids, extword_ids])
                else:
                    text = line.replace('##', '@@')
                    outputs = word_encoder.tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
                    bert_indices = outputs["input_ids"].squeeze()
                    segments_id = outputs["token_type_ids"].squeeze()
                    sent_len = min(max_sent_len, bert_indices.shape[0])
                    doc.append([sent_len, bert_indices[:max_sent_len], segments_id[:max_sent_len]])

    if len(doc) >= max_doc_len:
        examples.append([label2id(label), len(doc), doc])

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
    if shuffle: np.random.shuffle(data)
    batched_data.extend(list(batch_slice(data, batch_size)))

    if shuffle: np.random.shuffle(batched_data)
    for batch in batched_data:
        yield batch
