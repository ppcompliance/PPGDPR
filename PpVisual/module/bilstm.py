import torch
import torch.nn as nn
import torch.nn.functional as F
from .rnn_encoder import RNNEncoder


class BiLSTM(nn.Module):
    def __init__(self, args, vocab, embedding_weights):
        super(BiLSTM, self).__init__()

        embed_dim = embedding_weights.shape[1]

        self.word_embedding = nn.Embedding.from_pretrained(torch.from_numpy(embedding_weights))

        self._bidirectional = True
        self._nb_direction = 2 if self._bidirectional else 1
        self.lstm = RNNEncoder(input_size=embed_dim,   # 输入的特征维度
                               hidden_size=args.hidden_size,  # 隐层状态的特征维度
                               num_layers=args.nb_layer,
                               batch_first=True,
                               bidirectional=self._bidirectional,
                               dropout=args.rnn_dropout,
                               rnn_type='lstm')

        self.embed_drop = nn.Dropout(args.embed_dropout)
        self.linear_drop = nn.Dropout(args.linear_dropout)
        self.linear = nn.Linear(in_features=args.hidden_size * self._nb_direction,
                                out_features=vocab.label_size)

    def forward(self, inputs, mask):
        # [batch_size, max_seq_len] -> [batch_size, max_seq_len, embedding_dim]
        embed = self.word_embedding(inputs)

        if self.training:
            embed = self.embed_drop(embed)

        # rnn_out: [batch_size, max_seq_len, hidden_size * 2]
        # hidden: (h_n, c_n)  [1, batch_size, hidden_size * 2]
        rnn_out, hidden = self.lstm(embed, mask)

        # [batch_size, hidden_size * 2, max_seq_len]
        rnn_out.transpose_(1, 2)

        # [batch_size, hidden_size * 2, 1] -> [batch_size, hidden_size * 2]
        out = F.max_pool1d(rnn_out, kernel_size=rnn_out.size(2)).squeeze(2)

        if self.training:
            out = self.linear_drop(out)

        # [batch_size, 2]
        out = self.linear(out)

        return out

