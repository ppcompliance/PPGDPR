import sys
import os
sys.path.extend(["../../", "../", "./"])
# DIR = os.path.dirname(os.path.dirname(__file__))
#
# initfile = os.path.join(DIR, 'config\\att.cfg')
import argparse
from src.han_model import HanModel
from src.config import *
from src.trainer import Trainer
from src.vocab import Vocab
from src.gen import get_data

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


def get_han_result(file, model_file='/model/module_fold_6.bin'):
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('--config_file', default='./config/att.cfg')
    # argparser.add_argument('--w', default='lstm', help='word encoder')
    # argparser.add_argument('--s', default='lstm', help='sent encoder')
    # argparser.add_argument('--seed', default=666, type=int, help='seed')
    # argparser.add_argument('--gpu', default=7, type=int, help='gpu id')
    # argparser.add_argument('--model_name', default='han', help='model name')
    # argparser.add_argument('--epoch_num', default=0, help='model name')

    args = dict()
    args['config_file'] = "./att.cfg"
    args['w'] = 'lstm'
    args['s'] = 'lstm'
    args['seed'] = 666
    args['gpu'] = 0
    args['model_name'] = 'han'
    args['epoch_num'] = 0

    config = Config(args)

    torch.set_num_threads(config.threads)
    test_data = get_data(file, False)

    config.test_data = test_data

    # set cuda
    config.use_cuda = args['gpu'] >= 0 and torch.cuda.is_available()
    if config.use_cuda:
        torch.cuda.set_device(args['gpu'])
        config.device = torch.device("cuda")
    else:
        config.device = torch.device("cpu")
    logging.info("Use cuda: %s, gpu id: %d.", config.use_cuda, args['gpu'])

    # vocab

    vocab = Vocab(config.train_file)
    config.id2label = vocab.id2label
    # model
    model = HanModel(config, vocab, att_out=True)

    # trainer
    fold = str(args['config_file'].rstrip('.cfg')[-1])
    config.fold = fold

    trainer = Trainer(model, config, vocab, att_out=True, save_model=model_file)
    label_pred, w_att_result, s_att_result = trainer.att_test()

    origin_data = file.strip().split('\n')
    assert len(origin_data) == len(label_pred)

    # w_att_result = [[i] for i in w_att_result]
    return label_pred, origin_data, w_att_result



    # with open("w_att.json", "a+", encoding="utf8") as f:
    #     f.write('\n'.join(w_att_result))
    # with open("s_att.json", "a+", encoding="utf8") as f:
    #     f.write('\n'.join(s_att_result))
    # with open("label_att.json", "w", encoding="utf8") as f:
    #     f.write(json.dumps(label_pred))
