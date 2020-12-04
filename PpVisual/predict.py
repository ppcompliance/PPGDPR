import torch
import pickle
import os
# from module.bilstm_char import BiLSTM
from dataloader.Dataloader import batch_variable_with_char
from module.bilstm_char import BiLSTM
from conf import config
from vocab.Vocab import create_vocab, create_wc_vocab

def load_vocab(path):
    assert os.path.exists(path) and os.path.isfile(path)
    with open(path, 'rb') as fin:
        vocab = pickle.load(fin)
    return vocab


def load_model(path):
    assert os.path.exists(path) and os.path.isfile(path)

    # data_opts = config.data_path_parse('./conf/data_path.json')
    # vocab, char_vocab = create_wc_vocab(data_opts['data']['train_data'])
    # embedding_weights = vocab.get_embedding_weights(data_opts['data']['embedding_path'])
    # args = config.arg_parse()
    # model = BiLSTM(args, embedding_weights).to(args.device)
    # if args.enable_cuda and torch.cuda.is_available():
    #     args.device = torch.device('cuda', args.cuda)
    # else:
    #     args.device = torch.device('cpu')
    # print(args.device)
    # GPU上训练的模型在CPU上运行
    model = torch.load(path, map_location='cpu')
    # model.load_state_dict(path)
    # print("model load finish")
    model.eval()
    # print('eval finish')
    return model


def predict(pred_data, classifier, wd_vocab, char_vocab):
    # 按照batch进行预测
    vecwd_ids, char_ids, mask, _ = batch_variable_with_char(pred_data, wd_vocab, char_vocab)
    # [batch, nb_tags]
    pred = classifier(vecwd_ids, char_ids, mask)
    tag_idxs = torch.argmax(pred, dim=1)
    return wd_vocab.index2label(tag_idxs.tolist())


if __name__ == '__main__':
    # 加载词表
    char_vocab, wd_vocab = load_vocab("./model/word_vocab.pkl"), load_vocab("./model/word_vocab.pkl")
    # 加载模型
    classifier = load_model("./model/lstm_net.pkl")
    # 加载预测数据(封装成Instance对象, 无标签)
    pred_data = []
    # 传数据预测
    res = predict(pred_data, classifier, wd_vocab, char_vocab)
    print(res)
