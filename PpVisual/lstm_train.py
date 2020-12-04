#-*- coding : utf-8-*-

from conf import config
import torch
from dataloader.Dataloader import load_dataset, load_test_data

from vocab.Vocab import create_vocab, create_wc_vocab

# from module.cnn import TexCNN
# from module.bilstm import BiLSTM
from module.bilstm_char import BiLSTM
import logging
import numpy as np
from classifier import Classifier
import os
import pandas as pd
from dataloader.Dataloader import batch_variable_with_char
DIR = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(DIR, 'conf\\data_path.json')
from classifier import label_pred as label_pred
from module.bilstm_char import w_att_result
from src.gen import get_lstm_data

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)




def get_lstm_result(test_path):
    np.random.seed(666)
    torch.manual_seed(6666)
    torch.cuda.manual_seed(1234)
    # torch.cuda.manual_seed_all(4321)

    # print('GPU available: ', torch.cuda.is_available())
    # print('CuDNN available: ', torch.backends.cudnn.enabled)
    # print('GPU number: ', torch.cuda.device_count())

    data_opts = config.data_path_parse(initfile)

    # print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    # train_data = load_dataset(train_path)
    # dev_data = load_dataset
    test_data = [i.strip("\"").strip() for i in test_path.split('\n')]
    org_sentence = test_data
    test_data = get_lstm_data(test_data)


    test_data = [i.strip("\"").strip() for i in test_data]

    test_data = load_test_data(test_data)
    # print("--------------------------------------------------")
    # print('train_size=%d  dev_size=%d  test_size=%d' % (len(train_data), len(dev_data), len(test_data)))

    args = config.arg_parse()
    # args.use_cuda = torch.cuda.is_available()
    # if args.use_cuda and args.enable_cuda:
    #     torch.cuda.set_device(args.cuda)
    if args.enable_cuda and torch.cuda.is_available():
        args.device = torch.device('cuda', args.cuda)
    else:
        args.device = torch.device('cpu')
    # print(args.device)

    # vocab = create_vocab(data_opts['data']['train_data'])
    # print(data_opts['data']['train_data'])
    vocab, char_vocab = create_wc_vocab(DIR+"/data/privacypolicy/trainfiltedchange10000UTF.tsv")
    embedding_weights = vocab.get_embedding_weights(data_opts['data']['embedding_path'])
    vocab.save_vocab(data_opts['model']['save_vocab_path'])

    args.label_size = vocab.label_size
    args.char_vocab_size = char_vocab.vocab_size
    # model = TexCNN(args, vocab, embedding_weights).to(args.device)
    model = BiLSTM(args, embedding_weights).to(args.device)
    classifier = Classifier(model, args, vocab, char_vocab)
    classifier.summary()

    # classifier.cross_validate(model, train_data)

    classifier.load(DIR+'/model/lstm_net.pkl')
    # classifier.train(train_data, dev_data)

    # classifier.evaluate(test_data)


    # classifier.save(data_opts['model']['save_model_path'])

    print("model loaded")
    # print('test_data',test_data)
    classifier.predict(test_data)



    predictlabel = label_pred
    attention_word = w_att_result

    detectissues = []

    CollectPI = 0
    for sentlabel in predictlabel:
        # print(type(sentlabel))
        if sentlabel == 1:
            CollectPI = 1
            break

    if CollectPI == 1:
        for detectlabel in range(2, 10 + 1):
            havedetectlabel = 0
            for sentlabel in predictlabel:
                if sentlabel == detectlabel:
                    havedetectlabel = 1
            if havedetectlabel == 0:
                detectissues.append(detectlabel)

    # attword_str = []
    # for idx, org_sent in enumerate(org_sentence):
    #     if len(org_sent.split()) != np.size(attention_word[idx], 1):
    #         attendeal = attention_word[idx][0][1:(np.size(attention_word[idx], 1) - 1)]
    #         attword_str.append("[" + str(attendeal).replace("\n", "") + "]")
    #     else:
    #         attendeal = attention_word[idx][0][:]
    #         attword_str.append("[" + str(attendeal).replace("\n", "") + "]")
    # attention_word = [i.lstrip('[').rstrip(']').replace('\n', '') for i in attention_word]
    return predictlabel, org_sentence, attention_word, detectissues


if __name__ == '__main__':
    lab, org_s, att_w, detectiss = get_lstm_result("./data/privacypolicy/strawdogstudiosUTF.tsv")
    # label, orig, attention_w = get_han_result
    print(lab)
    print(org_s)
    print(att_w)
    print(detectiss)


