import sys

sys.path.extend(["../../", "../", "./"])
from pathlib import Path
import argparse
import pickle
from src.model import Model
from src.config import *
from src.trainer import Trainer
from src.vocab import Vocab

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')

import fitlog

fitlog.commit(__file__)  # auto commit your codes

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--config_file', default='bert.0.cfg')
    argparser.add_argument('--w', default='bert', help='word encoder')
    argparser.add_argument('--l', default='last', help='label encoder')
    argparser.add_argument('--seed', default=888, type=int, help='seed')
    argparser.add_argument('--gpu', default=0, type=int, help='gpu id')
    argparser.add_argument('--loss', default=0, type=int, help='gamma')
    argparser.add_argument('--fold', default=0, type=int, help='fold for test')
    args = argparser.parse_args()

    config = Config(args)
    assert args.loss == config.gamma
    torch.set_num_threads(config.threads)

    fitlog.add_hyper({'model': args.w, 'loss': config.gamma, 'fold': args.fold})

    # set cuda
    config.use_cuda = args.gpu >= 0 and torch.cuda.is_available()
    if config.use_cuda:
        torch.cuda.set_device(args.gpu)
        config.device = torch.device("cuda")
    else:
        config.device = torch.device("cpu")
    logging.info("Use cuda: %s, gpu id: %d.", config.use_cuda, args.gpu)

    # vocab
    cache_name = "./res/vocab_" + str(args.fold) + ".pickle"
    if Path(cache_name).exists():
        vocab_file = open(cache_name, 'rb')
        vocab = pickle.load(vocab_file)
        print('Load vocab from ' + cache_name)
    else:
        vocab = Vocab(config.train_file)
        file = open(cache_name, 'wb')
        pickle.dump(vocab, file)
        print('Cache vocab to ' + cache_name)

    # model
    model = Model(config, vocab)

    # trainer
    trainer = Trainer(model, config, vocab, fitlog)
    trainer.train()
    trainer.test()
