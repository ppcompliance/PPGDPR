#-*- coding : utf-8-*-

import copy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import time
from dataloader.Dataloader import cv_data_split, batch_variable, batch_variable_with_char, get_batch
import pickle
import os
DIR = os.path.dirname(os.path.abspath(__file__))
import torch.nn.functional as F
# import matplotlib.pyplot as plt


class History(object):
    def __init__(self):
        self.epochs = []
        # key: train_acc, train_loss, dev_acc, dev_loss
        # value: list type
        self.history = {}

    def dump(self, path):
        assert os.path.exists(path)
        with open(path, 'wb') as fw:
            pickle.dump(self, fw)

    # def load(self, path):
    #     with open(path, 'rb') as fin:
    #         return pickle.load(fin)

label_pred = []
origin_data = []
# w_att_result = []

class Classifier(object):
    def __init__(self, classify_model=None, args=None, vocab=None, char_vocab=None):
        super(Classifier, self).__init__()  # 对继承自父类的属性进行初始化
        assert isinstance(classify_model, nn.Module)
        self._classifier = classify_model
        self._args = args
        self._vocab = vocab
        self._char_vocab = char_vocab
        self._hist = None

    def summary(self):
        print(self._classifier)
        # print(self._classifier.state_dict())

    # k-folds 交叉验证
    def cross_validate(self, model, dataset, test_data, folds=9):
        test_acc_lst = []

        for i, (train_data, dev_data) in enumerate(cv_data_split(dataset, folds)):
            print('='*10, i, '='*10)
            # self._classifier = model  # 赋值，传对象的引用
            # self._classifier = copy.copy(model)  # 浅拷�? 只拷贝父对象, 不会拷贝对象的内部的子对�?            
            self._classifier = copy.deepcopy(model)  # 深拷�? 拷贝父对象及子对�?
            self.train(train_data, dev_data)

            test_acc = self.evaluate(test_data)
            test_acc_lst.append(test_acc)

        print('final acc: %.3f' % np.mean(test_acc_lst))

    def train(self, train_data, dev_data):
        # 优化器：更新模型参数
        optimizer = optim.Adam(filter(lambda p: p.requires_grad, self._classifier.parameters()),
                               lr=self._args.learning_rate,
                               weight_decay=self._args.weight_decay)

        # optimizer = optim.SGD(filter(lambda p: p.requires_grad, classifier.parameters()), lr=0.01, momentum=0.9)

        # optimizer = optim.Adadelta(filter(lambda p: p.requires_grad, classifier.parameters()),
        #                            weight_decay=self._args.weight_decay)

        self._hist = History()  # 保持训练过程的acc和loss
        train_acc_lst, train_loss_lst = [], []
        dev_acc_lst, dev_loss_lst = [], []
        # 迭代更新
        for i in range(self._args.epochs):
            self._classifier.train()

            start = time.time()
            train_acc, train_loss = 0, 0
            for j, train_batch_data in enumerate(get_batch(train_data, self._args.batch_size)):
                # 数据变量(Tensor)�?                
                batch_vecwd_ids, batch_char_ids, mask, batch_y = batch_variable_with_char(train_batch_data, self._vocab, self._char_vocab)

                batch_vecwd_ids = batch_vecwd_ids.to(self._args.device)
                batch_char_ids = batch_char_ids.to(self._args.device)
                mask = mask.to(self._args.device)
                batch_y = batch_y.to(self._args.device)

                # 梯度清零
                self._classifier.zero_grad()

                # 将数据喂给模型，预测输出(前向传播)
                pred = self._classifier(batch_vecwd_ids, batch_char_ids, mask)
                # print(pred)
                # 计算误差
                loss = self._calc_loss(pred, batch_y)  # 单元素的tensor
                acc_val = self._calc_acc(pred, batch_y)
                loss_val = loss.data.cpu().item()
                train_loss += loss_val
                train_acc += acc_val
                # print("[Train] epoch %d, batch %d  loss: %.3f acc: %.3f" % (i+1, j+1, loss_val, acc_val / len(train_batch_data)))

                # 误差反向传播，求梯度
                loss.backward()

                # 更新网络参数
                # for p in classifier.parameters():
                #     p.data -= self._args.learning_rate * p.grad.data

                optimizer.step()

            train_acc /= len(train_data)
            train_loss /= len(train_data)
            train_acc_lst.append(train_acc)
            train_loss_lst.append(train_loss)

            dev_acc, dev_loss = self._validate(dev_data)
            dev_acc_lst.append(dev_acc)
            dev_loss_lst.append(dev_loss)

            end = time.time()

            print("[Epoch%d] time: %.2fs train_loss: %.3f train_acc: %.3f  dev_loss: %.3f dev_acc: %.3f" %
                  (i + 1, (end - start), train_loss, train_acc, dev_loss, dev_acc))

            self._hist.epochs.append(i)

        self._hist.history['train_acc'] = train_acc_lst
        self._hist.history['train_loss'] = train_loss_lst
        self._hist.history['dev_acc'] = dev_acc_lst
        self._hist.history['dev_loss'] = dev_loss_lst

        # self._draw_hist()
        return self._hist

    def _validate(self, dev_data):
        self._classifier.eval()

        dev_acc, dev_loss = 0, 0
        for k, dev_batch_data in enumerate(get_batch(dev_data, self._args.batch_size)):
            with torch.no_grad():  # 确保在代码执行期间没有计算和存储梯度, 起到预测加速作�?                
                batch_vecwd_ids, batch_char_ids, mask, batch_y = batch_variable_with_char(dev_batch_data, self._vocab, self._char_vocab)

                batch_vecwd_ids = batch_vecwd_ids.to(self._args.device)
                batch_char_ids = batch_char_ids.to(self._args.device)
                mask = mask.to(self._args.device)
                batch_y = batch_y.to(self._args.device)

                pred = self._classifier(batch_vecwd_ids, batch_char_ids, mask)

                loss = self._calc_loss(pred, batch_y)
                acc_val = self._calc_acc(pred, batch_y)
                loss_val = loss.data.cpu().item()
                dev_acc += acc_val
                dev_loss += loss_val

        dev_acc /= len(dev_data)
        dev_loss /= len(dev_data)
        return dev_acc, dev_loss

    def evaluate(self, test_data):
        self._classifier.eval()
        test_acc = 0
        for test_batch_data in get_batch(test_data, self._args.batch_size, shuffle=False):
            batch_vecwd_ids, batch_char_ids, mask, batch_y = batch_variable_with_char(test_batch_data, self._vocab, self._char_vocab)

            batch_vecwd_ids = batch_vecwd_ids.to(self._args.device)
            batch_char_ids = batch_char_ids.to(self._args.device)
            mask = mask.to(self._args.device)
            batch_y = batch_y.to(self._args.device)

            pred = self._classifier(batch_vecwd_ids, batch_char_ids, mask)
            acc_val = self._calc_acc(pred, batch_y)
            test_acc += acc_val

        test_acc /= len(test_data)
        print("=== test acc: %.3f ===" % test_acc)
        return test_acc

    def _calc_acc(self, pred, target):
        return torch.eq(torch.argmax(pred, dim=1), target).cpu().sum().item()

    def _calc_loss(self, pred, target):
        # 损失函数：计算误差�?        
        loss_func = nn.CrossEntropyLoss()  # LogSoftmax + NLLLoss
        loss = loss_func(pred, target)
        return loss

    def _draw_hist(self):
        assert self._hist is not None
        plt.figure(figsize=(10, 10))
        plt.subplot(211)
        plt.title('Train Result')
        plt.plot(self._hist.epochs, self._hist.history['train_acc'], c='b', label='train_acc')
        plt.plot(self._hist.epochs, self._hist.history['dev_acc'], c='b', label='dev_acc', linestyle='--', marker='|')
        plt.xlabel('epoch')
        plt.ylabel('acc')
        plt.legend()
        plt.subplot(212)
        plt.plot(self._hist.epochs, self._hist.history['train_loss'], c='r', label='train_loss')
        plt.plot(self._hist.epochs, self._hist.history['dev_loss'], c='r', label='dev_loss', linestyle='--', marker='|')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend()
        plt.tight_layout()
        plt.show()

    # 保存模型
    def save(self, save_path, save_all=False):
        # assert os.path.exists(save_path)
        if save_all:
            torch.save(self._classifier, save_path)
        else:
            torch.save(self._classifier.state_dict(), save_path)

    # 加载模型
    def load(self, load_path, load_all=False):
        assert os.path.exists(load_path)
        if load_all:
            # GPU上训练的模型在CPU上运�?            
            self._classifier = torch.load(load_path, map_location='cpu')
        else:
            self._classifier.load_state_dict(torch.load(load_path, map_location='cpu'))
        self._classifier.eval()

    def predict(self, pred_data):
        # vecwd_ids, char_ids, mask, _ = batch_variable_with_char(pred_data, self._vocab, self._char_vocab)
        # pred = self._classifier(vecwd_ids, char_ids, mask)
        # lbls = torch.argmax(pred, dim=1)
        # return self._vocab.label2index(lbls.tolist())

        self._classifier.eval()

        resultwriter = open(DIR+"/predictresult/predict_result.tsv", 'w', encoding="utf-8")
        resultwriter.writelines("labelpredict\tlabelreal\tparagraph\n")
        for test_batch_data in get_batch(pred_data, self._args.batch_size):
            batch_vecwd_ids, batch_char_ids, mask, batch_y = batch_variable_with_char(test_batch_data, self._vocab,
                                                                                      self._char_vocab)

            batch_vecwd_ids = batch_vecwd_ids.to(self._args.device)
            batch_char_ids = batch_char_ids.to(self._args.device)
            mask = mask.to(self._args.device)
            batch_y = batch_y.to(self._args.device)
            pred = self._classifier(batch_vecwd_ids, batch_char_ids, mask)

            softmaxpre = F.softmax(pred)
            lbls = torch.argmax(pred, dim=1)
            for i in range(len(batch_y)):
                resultwriter.writelines(str(int(lbls[i])) + "\t" + str(int(batch_y[i])) + "\t" + "none" + "\n")
                label_pred.append(int(lbls[i]))
                softm = []
                softm.append(str(float(softmaxpre[i][int(lbls[i])])))
                # print(softmaxpre[i])
                # print(str(float(softmaxpre[i][int(lbls[i])])))
                # w_att_result.append(softm)
                # print("OK")
        # return self._vocab.label2index(lbls.tolist())
        # test_acc /= len(pred_data)
        # print("=== test acc: %.3f ===" % test_acc)



