import logging

from module import *
from module.layers import *

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class Model(nn.Module):
    def __init__(self, config, vocab):
        super(Model, self).__init__()

        self.all_parameters = {}
        parameters = []
        bert_parameters = None

        # encoder
        if config.word_encoder == 'lstm':
            self.word_encoder = WordEncoder(config, vocab)
            sent_rep_size = config.word_hidden_size * 2
            self.word_encoder.init_classifier(sent_rep_size, vocab.label_size)
            parameters.extend(list(filter(lambda p: p.requires_grad, self.word_encoder.parameters())))

        else:
            if config.word_encoder == 'bert':
                self.word_encoder = WordBertEncoder(config)
                sent_rep_size = 768
                self.word_encoder.init_classifier(sent_rep_size, vocab.label_size)

            bert_parameters = self.word_encoder.get_bert_parameters()
            parameters.extend(self.word_encoder.get_out_parameters())

        if config.use_cuda:
            self.word_encoder.to(config.device)

        if len(parameters) > 0:
            self.all_parameters["basic_parameters"] = parameters

        if bert_parameters is not None:
            self.all_parameters["bert_parameters"] = bert_parameters

        logging.info('Build model with {} encoder, {} label encoder.'.format(config.word_encoder,
                                                                             config.label_encoder))
        para_num = sum([np.prod(list(p.size())) for p in self.word_encoder.parameters()])
        logging.info('Model param num: %.2f M.' % (para_num / 1e6))

    def forward(self, word_inputs):
        # batch_inputs(batch_inputs1, batch_inputs2): sen_num x sent_len
        # batch_masks : sen_num x sent_len

        batch_outputs = self.word_encoder(word_inputs)  # sen_num x sent_rep_size

        return batch_outputs
