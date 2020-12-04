import logging
import os
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
initfile = os.path.join(DIR, 'config\\att.cfg')
import random
import configparser
from datetime import datetime

import numpy as np
import torch

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class Config(object):
    def __init__(self, args):
        self.word_encoder = args['w']
        self.sent_encoder = args['s']
        # self.gpu_id = args.gpu
        self.model_name = args['model_name']
        self.epoch_num = args['epoch_num']

        random.seed(args['seed'])
        np.random.seed(args['seed'])
        torch.cuda.manual_seed(args['seed'])
        torch.manual_seed(args['seed'])

        config_file = args['config_file']
        print("config_file", initfile)
        config = configparser.ConfigParser()
        config.read(initfile)

        self._config = config
        fold = str(args['config_file'].split('.')[1][-1])

        self.save_dir = './save/' + args['w'] + '.' + args['s'] + '.' + str(
            self.tune_start_layer) + '/' + datetime.now().strftime(r'%m%d_%H%M%S')
        # self.save_dir = './save/'
        self.log_dir = self.save_dir
        self.save_model = self.save_dir + '/module_fold_'+fold+'.bin'
        self.save_config = self.save_dir + '/bert.lstm.all.cfg'

        if self.save and not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)
            config.write(open(self.save_config, 'w'))

        logging.info('Load config file successfully.')
        # for section in config.sections():
        #     for k, v in config.items(section):
        #         print(k, v)

    @property
    def glove_path(self):
        return self._config.get('Data', 'glove_path')

    @property
    def bert_path(self):
        return self._config.get('Data', 'bert_path')

    @property
    def train_file(self):
        return self._config.get('Data', 'train_file')

    @property
    def dev_file(self):
        return self._config.get('Data', 'dev_file')

    @property
    def test_file(self):
        return self._config.get('Data', 'test_file')

    @property
    def save(self):
        return self._config.getboolean('Save', 'save')

    @property
    def tune_start_layer(self):
        return self._config.getint('Network', 'tune_start_layer')

    @property
    def cat_layers(self):
        return self._config.getint('Network', 'cat_layers')

    @property
    def word_dims(self):
        return self._config.getint('Network', 'word_dims')

    @property
    def dropout_embed(self):
        return self._config.getfloat('Network', 'dropout_embed')

    @property
    def dropout_mlp(self):
        return self._config.getfloat('Network', 'dropout_mlp')

    @property
    def sent_num_layers(self):
        return self._config.getint('Network', 'sent_num_layers')

    @property
    def word_num_layers(self):
        return self._config.getint('Network', 'word_num_layers')

    @property
    def word_hidden_size(self):
        return self._config.getint('Network', 'word_hidden_size')

    @property
    def sent_hidden_size(self):
        return self._config.getint('Network', 'sent_hidden_size')

    @property
    def dropout_input(self):
        return self._config.getfloat('Network', 'dropout_input')

    @property
    def dropout_hidden(self):
        return self._config.getfloat('Network', 'dropout_hidden')

    @property
    def word_attention_size(self):
        return self._config.getint('Network', 'word_attention_size')

    @property
    def word_output_bias(self):
        return self._config.getboolean('Network', 'word_output_bias')

    @property
    def sent_attention_size(self):
        return self._config.getint('Network', 'sent_attention_size')

    @property
    def sent_output_bias(self):
        return self._config.getboolean('Network', 'sent_output_bias')

    @property
    def learning_rate(self):
        return self._config.getfloat('Optimizer', 'learning_rate')

    @property
    def bert_lr(self):
        return self._config.getfloat('Optimizer', 'bert_lr')

    @property
    def decay(self):
        return self._config.getfloat('Optimizer', 'decay')

    @property
    def decay_steps(self):
        return self._config.getint('Optimizer', 'decay_steps')

    @property
    def beta_1(self):
        return self._config.getfloat('Optimizer', 'beta_1')

    @property
    def beta_2(self):
        return self._config.getfloat('Optimizer', 'beta_2')

    @property
    def epsilon(self):
        return self._config.getfloat('Optimizer', 'epsilon')

    @property
    def clip(self):
        return self._config.getfloat('Optimizer', 'clip')

    @property
    def threads(self):
        return self._config.getint('Run', 'threads')

    @property
    def epochs(self):
        return self._config.getint('Run', 'epochs')

    @property
    def train_batch_size(self):
        return self._config.getint('Run', 'train_batch_size')

    @property
    def test_batch_size(self):
        return self._config.getint('Run', 'test_batch_size')

    @property
    def log_interval(self):
        return self._config.getint('Run', 'log_interval')

    @property
    def early_stops(self):
        return self._config.getint('Run', 'early_stops')

    @property
    def save_after(self):
        return self._config.getint('Run', 'save_after')

    @property
    def update_every(self):
        return self._config.getint('Run', 'update_every')
