import pickle
import os
import numpy as np
from collections import Counter
from dataloader.Dataloader import load_dataset
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class WordVocab(object):
    def __init__(self, wd_counter, lbl_counter):
        self._min_count = 5
        self._UNK = 0

        self._wd2freq = {wd: count for wd, count in wd_counter.items() if count > self._min_count}

        self._wd2idx = {wd: idx+1 for idx, wd in enumerate(self._wd2freq.keys())}
        self._wd2idx['<unk>'] = self._UNK
        self._idx2wd = {idx: wd for wd, idx in self._wd2idx.items()}

        self._lbl2idx = {lbl: idx for idx, lbl in enumerate(lbl_counter.keys())}
        self._idx2lbl = {idx: lbl for lbl, idx in self._lbl2idx.items()}
        print('train_word_size:%d, label size:%d' % (len(self._wd2idx), len(self._lbl2idx)))

        self._vecwd2idx = dict()
        self._idx2vecwd = dict()

    # 构建词表方式：
    # 1、根据训练集中的词，构建索引词表，赋予一个预训练的词向量(OOV随机初始化)
    # 2、根据预训练词向量中的词，构建索引词表，赋予每个训练集中的词一个预训练词向量

    # 根据训练集构建：在与开发集、测试集(词)交集较小时不太适合，适用于训练集很大的情况
    # def get_embedding_weights(self, embed_path):
    #     # assert os.path.exists(embed_path)
    #     wd2vec_tab = {}
    #     vector_size = 0
    #     with open(embed_path, 'r', encoding='utf-8', errors='ignore') as fin:
    #         for line in fin:
    #             tokens = line.strip().split()
    #             if len(tokens) > 2:
    #                 wd, vec = tokens[0], tokens[1:]
    #                 vector_size = len(vec)
    #                 wd2vec_tab[wd] = np.asarray(vec, dtype=np.float32)
    #
    #     vocab_size = len(self._wd2idx)
    #     embedding_weights = np.zeros((vocab_size, vector_size), dtype=np.float32)
    #     oov_count = 0
    #     for wd, idx in self._wd2idx.items():
    #         try:
    #             embedding_weights[idx] = wd2vec_tab[wd]
    #         except KeyError:
    #             embedding_weights[idx] = np.random.uniform(-0.25, 0.25, vector_size)
    #             oov_count += 1
    #             pass
    #     print('oov ratio: %.3f%%' % (100 * oov_count / vocab_size))
    #
    #     return embedding_weights

    # 根据预训练词表构建
    def get_embedding_weights(self, embed_path):
        print("embed_path",embed_path)
        # assert os.path.exists(DIR+embed_path)
        wd2vec_tab = {}
        vector_size = 0
        with open(DIR+embed_path, 'r', encoding='utf-8', errors='ignore') as fin:
            for line in fin:
                tokens = line.strip().split()
                if len(tokens) > 2:
                    wd, vec = tokens[0], tokens[1:]
                    # wd = '<' + wd + '>'
                    vector_size = len(vec)
                    wd2vec_tab[wd] = np.array(vec, dtype=np.float32)

        self._vecwd2idx = {wd: idx for idx, wd in enumerate(wd2vec_tab.keys())}
        self._vecwd2idx['<unk>'] = self._UNK
        self._idx2vecwd = {idx: wd for wd, idx in self._vecwd2idx.items()}

        vocab_size = len(self._vecwd2idx)
        print('vocab size:', vocab_size)
        embedding_weights = np.zeros((vocab_size, vector_size), dtype=np.float32)
        for wd, idx in self._vecwd2idx.items():
            if idx != self._UNK:
                embedding_weights[idx] = wd2vec_tab[wd]

        oov_count = len([wd for wd in self._wd2idx.keys() if wd not in wd2vec_tab.keys()])
        print('oov ratio: %.3f%%' % (100 * oov_count / len(self._wd2idx)))
        embedding_weights[self._UNK] = np.mean(embedding_weights, 0) / np.std(embedding_weights)

        return embedding_weights

    def save_vocab(self, save_path):
        # assert os.path.exists(save_path)
        with open(DIR+save_path, 'wb') as fout:
            pickle.dump(self, fout)

    def word2index(self, wds):
        if isinstance(wds, list):
            return [self._wd2idx.get(wd, self._UNK) for wd in wds]
        else:
            return self._wd2idx.get(wds, self._UNK)

    def index2word(self, idxs):
        if isinstance(idxs, list):
            return [self._idx2wd.get(i, '<unk>') for i in idxs]
        else:
            return self._idx2wd.get(idxs, '<unk>')

    def vecword2index(self, wds):
        if isinstance(wds, list):
            return [self._vecwd2idx.get(wd, self._UNK) for wd in wds]
        else:
            return self._vecwd2idx.get(wds, self._UNK)

    def index2vecword(self, idxs):
        if isinstance(idxs, list):
            return [self._idx2vecwd.get(i, '<unk>') for i in idxs]
        else:
            return self._idx2vecwd.get(idxs, '<unk>')

    def label2index(self, lbls):
        if isinstance(lbls, list):
            return [self._lbl2idx.get(lbl, -1) for lbl in lbls]
        else:
            return self._lbl2idx.get(lbls, -1)

    def index2label(self, idxs):
        if isinstance(idxs, list):
            return [self._idx2lbl.get(i) for i in idxs]
        else:
            return self._idx2lbl.get(idxs)

    @property
    def vocab_size(self):
        return len(self._wd2idx)

    @property
    def vec_vocab_size(self):
        return len(self._vecwd2idx)

    @property
    def label_size(self):
        return len(self._lbl2idx)


class CharVocab(object):
    def __init__(self, chars_counter):
        self._UNK = 0
        self._PREFIX = 1
        self._SUFFIX = 2

        # self._alphabet = r'''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
        # -=+/\?.*&^%$#@!,;:"'`|~_()[]{}'''
        self._alphabet = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'''

        chars_counter.update(self._alphabet)

        # 为每个词添加prefix和suffix字符
        # good -> <good>
        self._char2idx = {ch: idx + 1 for idx, ch in enumerate(chars_counter.keys())}
        self._char2idx['<unk>'] = self._UNK
        # self._char2idx['<'] = self._PREFIX
        # self._char2idx['>'] = self._SUFFIX

        self._idx2char = {idx: ch for ch, idx in self._char2idx.items()}
        print('char vocab size:', len(self._char2idx))

    def char2index(self, chars):
        if isinstance(chars, list) or len(chars) > 1:
            return [self._char2idx.get(c, self._UNK) for c in chars]
        else:
            return self._char2idx.get(chars, self._UNK)

    def index2char(self, idxs):
        if isinstance(idxs, list):
            return [self._idx2char.get(i) for i in idxs]
        else:
            return self._idx2char.get(idxs)

    @property
    def vocab_size(self):
        return len(self._char2idx)


def create_vocab(path):
    assert os.path.exists(path)
    wds_counter, lbl_counter = Counter(), Counter()
    insts = load_dataset(path)
    for inst in insts:
        lbl_counter[inst.lbl] += 1
        for wd in inst.words:
            wds_counter[wd] += 1

    return WordVocab(wds_counter, lbl_counter)


def create_wc_vocab(path):
    assert os.path.exists(path)
    wds_counter, lbl_counter = Counter(), Counter()
    chars_counter = Counter()
    insts = load_dataset(path)
    for inst in insts:
        lbl_counter[inst.lbl] += 1
        for wd in inst.words:
            wds_counter[wd] += 1
            chars_counter.update(wd)

    return WordVocab(wds_counter, lbl_counter), CharVocab(chars_counter)
