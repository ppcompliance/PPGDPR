import logging

from module.layers import *

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class Encoder(nn.Module):
    def __init__(self, dropout_mlp):
        super(Encoder, self).__init__()
        self.dropout = nn.Dropout(dropout_mlp)

    def init_classifier(self, sent_rep_size, label_size):
        self.out = NoLinear(sent_rep_size, label_size, bias=True)

    def get_out_parameters(self):
        parameters = list(filter(lambda p: p.requires_grad, self.out.parameters()))

        return parameters

    def get_bert_parameters(self):
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_parameters = [
            {'params': [p for n, p in self.bert.named_parameters() if not any(nd in n for nd in no_decay)],
             'weight_decay': 0.01},
            {'params': [p for n, p in self.bert.named_parameters() if any(nd in n for nd in no_decay)],
             'weight_decay': 0.0}
        ]
        return optimizer_parameters

    def last_pooling(self, inputs, masks):
        # inputs  sen_num x sent_len x hidden float32
        # masks   sen_num x sent_len          float32

        index = torch.sum(masks, 1).long() - 1  # last step

        batch_res = []
        for i in range(inputs.shape[0]):
            batch_res.append(torch.index_select(inputs[i], 0, index[i]))  # hidden*2

        reps = torch.cat(batch_res, 0)  # sen_num x hidden*2

        return reps
