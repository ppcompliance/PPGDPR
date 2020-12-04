from transformers import BertTokenizer, BertModel

from module.layers import *


class WordBertEncoder(nn.Module):
    def __init__(self, config):
        super(WordBertEncoder, self).__init__()
        self.tokenizer = BertTokenizer.from_pretrained(config.bert_path)
        self.bert = BertModel.from_pretrained(config.bert_path)
        self.bert.encoder.output_hidden_states = True

        self.tune_start_layer = config.tune_start_layer
        self.cat_layers = config.cat_layers

        self.bert_layers = self.bert.config.num_hidden_layers
        if self.tune_start_layer >= self.bert_layers: self.tune_start_layer = self.bert_layers

        self.mlp_word = NoLinear(768 * self.cat_layers, config.word_hidden_size * 2, activation=GELU())

        for p in self.bert.named_parameters():
            # print(p[0]) name
            p[1].requires_grad = False
        for p in self.bert.named_parameters():
            items = p[0].split('.')
            if len(items) < 3: continue
            if items[0] == 'embeddings' and 0 >= self.tune_start_layer: p[1].requires_grad = True
            if items[0] == 'encoder' and items[1] == 'layer':
                layer_id = int(items[2]) + 1
                if layer_id >= self.tune_start_layer: p[1].requires_grad = True

    def forward(self, batch_inputs1, batch_inputs2):
        # batch_inputs1 indices: sen_num x sent_len
        # batch_inputs2 segments: sen_num x sent_len

        all_hidden_states = self.bert(batch_inputs1, batch_inputs2)[2]  # (sen_num x sent_len x cls_dims * 13)

        index = torch.LongTensor([0]).to(all_hidden_states[0].device)  # cls index
        all_cls_states = list(
            map(lambda x: torch.index_select(x, 1, index).squeeze(1), all_hidden_states[-self.cat_layers:]))
        # list [sen_num x cls_dims] * last n layers, n = self.cat_layers

        sent_reps = torch.cat(all_cls_states, 1)  # sen_num x 768*self.cat_layers
        mlp_sent_reps = self.mlp_word(sent_reps)  # sen_num x word_hidden_size*2

        return mlp_sent_reps
