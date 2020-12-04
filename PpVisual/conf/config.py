#-*- coding : utf-8-*-
import os
import argparse
import json
import logging


# debug info warning error
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)', level=logging.INFO)


class Config:
    def __init__(self):
        self.cuda = -1
        self.enable_cuda = False
        self.bz = 1
        self.ep = 1
        self.hz = 200
        self.nb_layer = 2
        self.embed_dropout = 0.5
        self.rnn_dropout = 0.0
        self.linear_dropout = 0.5
        self.chz = 200
        self.char_embed_dim = 50
        self.lr = 3e-3
        self.wd = 1e-7


# 语料路径解析
def data_path_parse(path):
    print(path)
    assert os.path.exists(path)
    with open(path, 'r', encoding='utf-8') as fin:
        opts = json.load(fin)  # 读取json文件，写json文件是json.dump()

    # logging.info(opts)
    # print(opts)

    return opts


# 参数解析
def arg_parse():
    # parser = argparse.ArgumentParser(description="CNN Arguments Configuration")
    # 通用配置
    # parser.add_argument('--cuda', type=int, default=0, help='-1 means train on CPU')
    # # parser.add_argument('--use_cuda', type=bool, default=True, help='use GPU or not')
    # parser.add_argument('--enable_cuda', type=bool, default=True, help='enable GPU or not')
    #
    # # 配置数据参数
    # parser.add_argument('-bz', '--batch_size', type=int, default=1, help='the size of per batch')
    # parser.add_argument('-ep', '--epochs', type=int, default=1, help='the number of iter')
    #
    # # 配置模型参数
    # parser.add_argument('-hz', '--hidden_size', type=int, default=200, help='the size of hidden layer')
    # parser.add_argument('--nb_layer', type=int, default=2, help='the number of hidden layer')
    # parser.add_argument('--embed_dropout', type=float, default=0.5, help='the dropout of embedding layer')
    # # *rnn_dropout对结果影响较�?
    # parser.add_argument('--rnn_dropout', type=float, default=0.0, help='the dropout of recurrent layer')
    # parser.add_argument('--linear_dropout', type=float, default=0.5, help='the dropout of linear layer')
    # # char embedding
    # parser.add_argument('-chz', '--char_hidden_size', type=int, default=200, help='the size of char embedding layer')
    # parser.add_argument('--char_embed_dim', type=int, default=50, help='the initialed char embedding size')
    #
    # # 配置优化器参�?
    # parser.add_argument('-lr', '--learning_rate', type=float, default=3e-3, help='leaning rate in training')
    # # 权值衰减系数，L2正则化参�?
    # parser.add_argument('-wd', '--weight_decay', type=float, default=1e-7, help='weight decay')

    # # parser.add_argument('-m', type=str, default="flask run")

    config = Config
    config.cuda = -1

    config.enable_cuda = False
    config.bz = 1
    config.batch_size = config.bz
    config.ep = 1
    config.epochs = config.ep
    config.hz = 200
    config.hidden_size = config.hz
    config.nb_layer = 2
    config.embed_dropout = 0.5
    config.rnn_dropout = 0.0
    config.linear_dropout = 0.5
    config.chz = 200
    config.char_hidden_size = config.chz
    config.char_embed_dim = 50
    config.lr = 3e-3
    config.learning_rate = config.lr
    config.wd = 1e-7
    config.weight_decay = config.wd

    # print(vars(args))

    return config
