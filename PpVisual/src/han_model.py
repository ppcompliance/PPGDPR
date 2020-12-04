import logging
import json
from module.attention import *
from module.layers import *
from module.sent_encoder import SentEncoder
from module.word_bert_encoder import WordBertEncoder
from module.word_encoder import WordEncoder

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class HanModel(nn.Module):
    def __init__(self, config, vocab, att_out=False):
        super(HanModel, self).__init__()
        self.sent_rep_size = config.word_hidden_size * 2
        self.doc_rep_size = self.sent_rep_size if config.sent_encoder == 'avg' else config.sent_hidden_size * 2
        self.parameters = {}
        self.sent_encoder_flag = config.sent_encoder
        parameters = []
        bert_parameters = None
        if config.word_encoder == 'bert':
            self.word_encoder = WordBertEncoder(config)
            bert_parameters = list(filter(lambda p: p.requires_grad, self.word_encoder.parameters()))
        else:
            self.word_encoder = WordEncoder(config, vocab)
            self.word_attention = Attention(self.sent_rep_size, config.dropout_mlp)
            parameters.extend(list(filter(lambda p: p.requires_grad, self.word_encoder.parameters())))
            parameters.extend(list(filter(lambda p: p.requires_grad, self.word_attention.parameters())))

        if config.sent_encoder == 'lstm':
            self.sent_encoder = SentEncoder(config)
            self.sent_attention = Attention(self.doc_rep_size, config.dropout_mlp)
            parameters.extend(list(filter(lambda p: p.requires_grad, self.sent_encoder.parameters())))
            parameters.extend(list(filter(lambda p: p.requires_grad, self.sent_attention.parameters())))

        elif config.sent_encoder == 'att':
            self.sent_attention = Attention(config.word_hidden_size * 2, config.dropout_mlp)
            parameters.extend(list(filter(lambda p: p.requires_grad, self.sent_attention.parameters())))
        else:
            self.sent_encoder = None

        self.out = NoLinear(self.doc_rep_size, vocab.label_size, bias=True)

        if config.use_cuda:
            self.to(config.device)

        if len(parameters) > 0:
            self.parameters["basic_parameters"] = parameters

        if bert_parameters is not None:
            self.parameters["bert_parameters"] = bert_parameters

        self.att_out = att_out

        logging.info('Build Han model with {} word encoder, {} sent encoder successfully.'.format(config.word_encoder,
                                                                                                  config.sent_encoder))

    def forward(self, batch_inputs, batch_masks, att_file="./att.txt"):
        # batch_inputs(batch_inputs1, batch_inputs2): b x doc_len x sent_len
        # batch_masks : b x doc_len x sent_len
        batch_inputs1, batch_inputs2 = batch_inputs
        batch_size, max_doc_len, max_sent_len = batch_inputs1.shape[0], batch_inputs1.shape[1], batch_inputs1.shape[2]
        batch_inputs1 = batch_inputs1.view(batch_size * max_doc_len, max_sent_len)  # sen_num x sent_len
        batch_inputs2 = batch_inputs2.view(batch_size * max_doc_len, max_sent_len)  # sen_num x sent_len
        batch_masks = batch_masks.view(batch_size * max_doc_len, max_sent_len)  # sen_num x sent_len

        # batch_inputs = torch.zeros((batch_size, max_doc_len, self.sent_rep_size), requires_grad=True)  # b x len x hidden
        if isinstance(self.word_encoder, WordEncoder):
            batch_hiddens = self.word_encoder(batch_inputs1, batch_inputs2,
                                              batch_masks)  # sen_num x sent_len x sent_rep_size
            sent_reps, w_atten_scores = self.word_attention(batch_hiddens, batch_masks)  # sen_num x sent_rep_size
        else:
            sent_reps = self.word_encoder(batch_inputs1, batch_inputs2)  # sen_num x sent_rep_size

        sent_reps = sent_reps.view(batch_size, max_doc_len, self.sent_rep_size)  # b x doc_len x sent_rep_size
        batch_masks = batch_masks.view(batch_size, max_doc_len, max_sent_len)  # b x doc_len x max_sent_len
        sent_masks = batch_masks.bool().any(2).float()  # b x doc_len

        if self.sent_encoder_flag == "lstm":
            sent_hiddens = self.sent_encoder(sent_reps, sent_masks)  # b x doc_len x doc_rep_size
            doc_reps, s_atten_scores = self.sent_attention(sent_hiddens, sent_masks)  # b x doc_rep_size
        elif self.sent_encoder_flag == "att":
            doc_reps, s_atten_scores = self.sent_attention(sent_reps, sent_masks)
        else:
            avg_sent_masks = sent_masks / torch.sum(sent_masks, 1, True)  # b x doc_len
            doc_reps = torch.bmm(avg_sent_masks.unsqueeze(1), sent_reps).squeeze(1)  # b x doc_rep_size

        batch_outputs = self.out(doc_reps)  # b x num_labels
        if self.att_out:
            return batch_outputs, w_atten_scores, s_atten_scores

        return batch_outputs
