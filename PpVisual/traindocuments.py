from conf import config
from dataloader.Dataloader import load_dataset
from vocab.Vocab import create_vocab, create_wc_vocab
import torch
# from module.cnn import TexCNN
# from module.bilstm import BiLSTM
from module.bilstm_char import BiLSTM
import logging
import numpy as np
from classifier import Classifier
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

from dataloader.Dataloader import batch_variable_with_char

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)



# def predict(pred_data, classifier, wd_vocab, char_vocab):
#     # 按照batch进行预测
#     vecwd_ids, char_ids, mask, _ = batch_variable_with_char(pred_data, wd_vocab, char_vocab)
#     # [batch, nb_tags]
#     pred = classifier(vecwd_ids, char_ids, mask)
#     tag_idxs = torch.argmax(pred, dim=1)
#     return wd_vocab.index2label(tag_idxs.tolist())



if __name__ == '__main__':
    # 设置随机种子(固定随机值)
    np.random.seed(666)
    torch.manual_seed(6666)
    torch.cuda.manual_seed(1234)  # 为当前GPU设置种子
    # torch.cuda.manual_seed_all(4321)  # 为所有GPU设置种子(如果有多个GPU)

    print('GPU available: ', torch.cuda.is_available())
    print('CuDNN available: ', torch.backends.cudnn.enabled)
    print('GPU number: ', torch.cuda.device_count())

    # 加载数据(训练集-学习、开发集-调参、测试集-评估)
    data_opts = config.data_path_parse('./conf/data_path.json')
    train_data = load_dataset(data_opts['data']['train_data'])
    dev_data = load_dataset(data_opts['data']['dev_data'])
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    test_data = load_dataset(data_opts['data']['test_data'])
    # print("--------------------------------------------------")
    print('train_size=%d  dev_size=%d  test_size=%d' % (len(train_data), len(dev_data), len(test_data)))

    # 设置参数(数据参数+模型参数)
    args = config.arg_parse()
    # args.use_cuda = torch.cuda.is_available()
    # if args.use_cuda and args.enable_cuda:
    #     torch.cuda.set_device(args.cuda)
    if args.enable_cuda and torch.cuda.is_available():
        args.device = torch.device('cuda', args.cuda)
    else:
        args.device = torch.device('cpu')
    print(args.device)

    # 创建词表
    #vocab = create_vocab(data_opts['data']['train_data'])
    vocab, char_vocab = create_wc_vocab(data_opts['data']['train_data'])
    embedding_weights = vocab.get_embedding_weights(data_opts['data']['embedding_path'])
    vocab.save_vocab(data_opts['model']['save_vocab_path'])

    # 构建分类模型
    args.label_size = vocab.label_size
    args.char_vocab_size = char_vocab.vocab_size
    # model = TexCNN(args, vocab, embedding_weights).to(args.device)
    model = BiLSTM(args, embedding_weights).to(args.device)
    classifier = Classifier(model, args, vocab, char_vocab)
    classifier.summary()

    # 训练
    classifier.train(train_data, dev_data)

    # 评估
    classifier.evaluate(test_data)

    # 保存
    # print(data_opts['model']['save_model_path'])
    classifier.save(data_opts['model']['save_model_path'])



    classifier.predict(test_data)
    # print(p)
    # print(len(p))
    # res = predict(test_data, classifier, vocab, char_vocab)
    # print(res)