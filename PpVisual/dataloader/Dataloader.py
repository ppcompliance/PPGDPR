


import numpy as np
import torch

class Instance(object):
    def __init__(self, words=None, lbl=None):
        self.words = words
        self.lbl = lbl

def load_dataset(data_path):
    insts = []
    with open(data_path, 'r', encoding='utf-8', errors='ignore') as fin:
    # with open(data_path, 'r', encoding='utf-8') as fin:
        for idx, line in enumerate(fin):
            if idx == 0:
                print("skip first line")
            else:
                lbl, sent = line.strip().split('\t')
                lbl, words = lbl.strip(), sent.strip().split()

                # tokens = line.strip().split(' ')
                # lbl, words = tokens[0].split(':')[0], tokens[1:]

                # words = ['<'+wd+'>' for wd in words]  # 添加字符前后缀
                # print(lbl)
                insts.append(Instance(words, int(lbl.replace("\"", ""))))

    # np.random.shuffle(insts)

    return insts

def load_test_data(fin):
    insts = []

    for idx, line in enumerate(fin):
        # if idx == 0:
        #     print("skip first line")
        # else:
        lbl, sent = line.strip().split('\t')
        lbl, words = lbl.strip(), sent.strip().split()

        # tokens = line.strip().split(' ')
        # lbl, words = tokens[0].split(':')[0], tokens[1:]

        # words = ['<'+wd+'>' for wd in words]  # 添加字符前后缀
        # print(lbl)
        insts.append(Instance(words, int(lbl.replace("\"", ""))))

    # np.random.shuffle(insts)

    return insts


def get_batch(dataset, batch_size, shuffle=False):
    if shuffle:
        np.random.shuffle(dataset)

    nb_batch = int(np.ceil(len(dataset) / batch_size))  # 向上取整
    for i in range(nb_batch):
        batch_data = dataset[i*batch_size: (i+1)*batch_size]
        if shuffle:
            np.random.shuffle(batch_data)

        yield batch_data


# k-fold 交叉验证数据分割(训练集：开发集：测试集 = 8�?�?)
def cv_data_split(dataset, folds):
    np.random.shuffle(dataset)

    nb_samples = int(np.ceil(len(dataset) / folds))
    for i in range(folds):
        val_samples = dataset[i * nb_samples: (i + 1) * nb_samples]
        if i < folds - 1:

            # 垂直方向进行拼接(数据维度要一�?
            # train_samples = np.vstack((dataset[:i * nb_samples], dataset[(i + 2) * nb_samples:]))
            train_samples = dataset[:i * nb_samples] + dataset[(i + 1) * nb_samples:]
        else:
            # test_samples = dataset[: nb_samples]
            # train_samples = np.vstack((dataset[nb_samples: (folds-1)*nb_samples]))
            train_samples = dataset[: (folds - 1) * nb_samples]
        yield train_samples, val_samples


def batch_variable(batch_data, vocab):
    batch_size = len(batch_data)
    max_seq_len = max([len(inst.words) for inst in batch_data])

    # 词索引需要时long�?    
    # wd_ids = torch.zeros(batch_size, max_seq_len, dtype=torch.long)
    vecwd_ids = torch.zeros((batch_size, max_seq_len), dtype=torch.long)
    targets = torch.zeros(batch_size, dtype=torch.long)
    mask = torch.zeros(batch_size, max_seq_len)

    for i, inst in enumerate(batch_data):
        seq_len = len(inst.words)
        # wd_ids[i, :seq_len] = torch.tensor(vocab.word2index(inst.words))
        vecwd_ids[i, :seq_len] = torch.tensor(vocab.vecword2index(inst.words))
        targets[i] = torch.tensor(inst.lbl)
        mask[i, :seq_len].fill_(1)

    return vecwd_ids, mask, targets


def batch_variable_with_char(batch_data, vocab, char_vocab):
    batch_size = len(batch_data)
    # max_seq_len = max([len(inst.words) for inst in batch_data])
    max_seq_len, max_wd_len = 0, 0
    for inst in batch_data:
        seq_len, wd_len = len(inst.words), max(map(len, inst.words))
        if seq_len > max_seq_len:
            max_seq_len = seq_len
        if wd_len > max_wd_len:
            max_wd_len = wd_len

    # for inst in batch_data:
    #     if len(inst.words) > max_seq_len:
    #         max_seq_len = len(inst.words)
    #     for wd in inst.words:
    #         if len(wd) > max_wd_len:
    #             max_wd_len = len(wd)

    max_wd_len = min(max_wd_len, 20)  # 限定最大单词长�?
    # wd_ids = torch.zeros(batch_size, max_seq_len, dtype=torch.long)
    vecwd_ids = torch.zeros((batch_size, max_seq_len), dtype=torch.long)
    char_ids = torch.zeros((batch_size, max_seq_len, max_wd_len), dtype=torch.long)
    targets = torch.zeros(batch_size, dtype=torch.long)
    mask = torch.zeros(batch_size, max_seq_len)

    for i, inst in enumerate(batch_data):
        seq_len = len(inst.words)
        # wd_ids[i, :seq_len] = torch.tensor(vocab.word2index(inst.words))
        vecwd_ids[i, :seq_len] = torch.tensor(vocab.vecword2index(inst.words))
        targets[i] = inst.lbl
        mask[i, :seq_len].fill_(1)
        for j, wd in enumerate(inst.words):
            l = min(len(wd), max_wd_len)
            char_ids[i, j, :l] = torch.tensor(char_vocab.char2index(wd[:l]))
            
    return vecwd_ids, char_ids, mask, targets
