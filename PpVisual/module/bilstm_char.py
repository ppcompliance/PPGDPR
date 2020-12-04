# -*- coding : utf-8-*-
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from .rnn_encoder import RNNEncoder
from .char_embed import CharEmbed
from module.AttentionLayer import Attention

w_att_result = []

# 绝对位置向量
class PositionEmbed(nn.Module):
    def __init__(self, embed_dim):
        super(PositionEmbed, self).__init__()
        # self._embed_dim = embed_dim
        # 注册一个持久化的buffer（不作为模型参数进行更新??        # self.register_buffer("pe", 1./torch.pow(10000, torch.arange(0.0, embed_dim, 2.0) / embed_dim))
        self.register_buffer("pe", 1. / torch.pow(10000, 2 * torch.arange(0.0, embed_dim / 2) / embed_dim))

    def forward(self, pos_seqs):
        '''
        :param pos_seqs: FloatTensor tensor([0, 1, 2, ..., seq_len-1])
        :return: position embedding:  [pos_seq_len, batch_size, pos_embed]
        '''
        batch_size = pos_seqs.size(0)
        pos_embeddings = []
        for i in range(batch_size):
            pos_embed = torch.ger(pos_seqs[i], self.pe)  # 向量外积
            pos_embed = torch.cat((torch.sin(pos_embed), torch.cos(pos_embed)), dim=-1)
            pos_embeddings.append(pos_embed)

        return torch.stack(tuple(pos_embeddings), dim=0)


class BiLSTM(nn.Module):
    def __init__(self, args, embedding_weights):
        super(BiLSTM, self).__init__()

        embed_dim = embedding_weights.shape[1]

        self.word_embedding = nn.Embedding.from_pretrained(torch.from_numpy(embedding_weights))
        # self.word_embedding.weight.data.copy_(torch.from_numpy(embedding_weights))
        # self.word_embedding.weight = nn.Parameter(torch.from_numpy(embedding_weights), requires_grad=False)
        self.word_embedding.weight.requires_grad = False

        self.char_embedding = CharEmbed(char_vocab_size=args.char_vocab_size,
                                        char_embedding_dim=args.char_embed_dim,
                                        char_hidden_size=args.char_hidden_size,
                                        dropout=0.5)

        self._bidirectional = True
        self._nb_direction = 2 if self._bidirectional else 1
        self._rnn_type = 'lstm'
        self.lstm = RNNEncoder(input_size=embed_dim + args.char_hidden_size,
                               hidden_size=args.hidden_size,
                               num_layers=args.nb_layer,
                               batch_first=True,
                               bidirectional=self._bidirectional,
                               dropout=args.rnn_dropout,
                               rnn_type=self._rnn_type)

        self.embed_drop = nn.Dropout(args.embed_dropout)
        self.linear_drop = nn.Dropout(args.linear_dropout)
        self.linear = nn.Linear(in_features=args.hidden_size * self._nb_direction,
                                out_features=args.label_size)
        self.attentionlayer = Attention(400, 0.0)

    def _attention(self, hidden_n, encoder_output, mask=None):

        scale = 1. / math.sqrt(hidden_n.size(1))  # 调节因子

        # # [batch_size, seq_len, hidden_size] * [batch_size, hidden_size, 1]
        # # -> [batch_size, seq_len, 1] -> [batch_size, seq_len]
        # att_weights = torch.bmm(encoder_output, hidden_n.unsqueeze(-1)).squeeze(-1)
        # if mask is not None:
        #     att_weights.mul_(mask)
        # soft_att_weights = F.softmax(att_weights.mul(scale), dim=1)  # [batch_size, seq_len]
        # # [batch_size, hidden_size, seq_len] * [batch_size, seq_len, 1] -> [batch_size, hidden_size]
        # att_out = torch.bmm(encoder_output.transpose(1, 2), soft_att_weights.unsqueeze(-1)).squeeze(-1)

        # [batch_size, 1, hidden_size] * [batch_size, hidden_size, seq_len]
        # -> [batch_size, 1, seq_len] -> [batch_size, seq_len]
        att_weights = torch.bmm(hidden_n.unsqueeze(1), encoder_output.transpose(1, 2)).squeeze(1)
        if mask is not None:
            att_weights.mul_(mask)
        soft_att_weights = F.softmax(att_weights.mul(scale), dim=1)  # [batch_size, seq_len]
        # [batch_size, 1, seq_len] * [batch_size, seq_len, hidden_size]
        # -> [batch_size, 1, hidden_size]
        att_out = torch.bmm(soft_att_weights.unsqueeze(1), encoder_output).squeeze(1)

        # print(soft_att_weights)
        # print(type(soft_att_weights))
        # print(len(att_out[1]))
        return att_out, soft_att_weights

    def forward(self, wds_input, chars_input, mask):
        # [batch_size, max_seq_len] -> [batch_size, max_seq_len, embedding_dim]
        wd_embed = self.word_embedding(wds_input)
        char_embed = self.char_embedding(chars_input)
        embed = torch.cat((wd_embed, char_embed), dim=2)

        if self.training:
            embed = self.embed_drop(embed)

        # rnn_out: [batch_size, max_seq_len, hidden_size * num_directions]
        # hidden: (h_n, c_n)  [num_layers, batch_size, hidden_size * num_directions]
        # print(mask)
        rnn_out, hidden_n = self.lstm(embed, mask)
        # print(rnn_out.size())
        # print(rnn_out.size())

        # print(sent_reps.size())
        # print(atten_scores.size())
        # print(atten_scores)

        # if self._rnn_type.lower() == 'lstm':
        #     hidden_n = hidden_n[0]

        # print(hidden_n[-1].size())
        # print(rnn_out.size())
        att_out, soft_att_weights = self.attentionlayer(rnn_out, mask)

        # print(att_out.size())
        soft_att_weights_round = np.around(soft_att_weights.detach().numpy(), decimals=3).tolist()
        w_att_result.append(str(soft_att_weights_round))
        # w_att_result.append(soft_att_weights.detach().numpy())

        #out, _ = self._attention(hidden_n[-1], rnn_out, mask)

        # print(out.size())
        # print(out)
        # print(out.size())
        # print(sent_reps)
        # print(sent_reps.size())
        # print(out)
        # print(out.size())
        # [batch_size, hidden_size * 2, max_seq_len]
        # -> [batch_size, hidden_size * 2, 1]
        # -> [batch_size, hidden_size * 2]
        # out = F.max_pool1d(rnn_out.transpose(1, 2), kernel_size=rnn_out.size(2)).squeeze(2)

        if self.training:
            att_out = self.linear_drop(att_out)

        # [batch_size, 2]
        att_out = self.linear(att_out)

        # print(out)
        return att_out

