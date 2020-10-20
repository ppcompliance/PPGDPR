import logging

from transformers import BertTokenizer, BertModel

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')
from module.encoder import Encoder


class WordBertEncoder(Encoder):
    def __init__(self, config):
        super(WordBertEncoder, self).__init__(config.dropout_mlp)
        self.tokenizer = BertTokenizer.from_pretrained(config.bert_path)
        self.bert = BertModel.from_pretrained(config.bert_path)

        self.pooled = False
        logging.info('Build Bert encoder with pooled {}.'.format(self.pooled))

    def forward(self, batch_inputs):
        # batch_inputs : sen_num x bert_len
        # batch_inputs : sen_num x basic_len x bert_len

        bert_inputs, bert_pieces, batch_masks = batch_inputs

        sequence_output, pooled_output = self.bert(bert_inputs)  # 2 is (sen_num x bert_len x cls_dims * 13)

        if self.pooled:
            reps = pooled_output
        else:
            reps = sequence_output[:, 0, :]  # sen_num x 768

        if self.training:
            reps = self.dropout(reps)

        outputs = self.out(reps)

        return outputs

    def bert2basic(self, text, max_len):
        text = text.replace('##', '@@')
        list_bert_indice = self.tokenizer.encode(text, add_special_tokens=True)

        basic_tokens = self.tokenizer.basic_tokenizer.tokenize(text, never_split=self.tokenizer.all_special_tokens)
        bert_tokens = self.tokenizer.convert_ids_to_tokens(list_bert_indice)

        bert_len, basic_token_len = len(bert_tokens), len(basic_tokens)

        if bert_tokens[-1] == "[SEP]":
            bert_len -= 1

        list_basic_id = []
        start_bert_id = 1

        for idx in range(basic_token_len):
            # basic token ==> UNK, one-one map
            if bert_tokens[start_bert_id] == "[UNK]":
                list_basic_id.append([start_bert_id])
                start_bert_id += 1
                continue

            cur_basic_token, cur_token_len = basic_tokens[idx], len(basic_tokens[idx])
            end_bert_id = start_bert_id
            sub_token = ""
            while end_bert_id < bert_len and len(sub_token) < cur_token_len:
                cur_sub_token = bert_tokens[end_bert_id]
                if cur_sub_token.startswith("##"): cur_sub_token = cur_sub_token[2:]
                sub_token = sub_token + cur_sub_token
                end_bert_id += 1

            if len(sub_token) == cur_token_len:
                cur_pieces = [piece_id for piece_id in range(start_bert_id, end_bert_id)]
                start_bert_id = end_bert_id
                list_basic_id.append(cur_pieces)
            else:
                print("bug here, basic token, not matched")

            if sub_token != cur_basic_token:
                print("please check, bert tokenizer changes something")

        if len(list_basic_id) > max_len:
            list_basic_id = list_basic_id[:max_len]
            last_bert_indice = list_basic_id[-1][-1]
            list_bert_indice = list_bert_indice[:last_bert_indice + 1] + list_bert_indice[-1:]

        return list_bert_indice, list_basic_id
