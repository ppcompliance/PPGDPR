import torch
import torch.nn as nn
import torch.nn.functional as F
# from .rnn_encoder import RNNEncoder


# 提取词的字符特征
class CharEmbed(nn.Module):
    def __init__(self, char_vocab_size,
                 char_embedding_dim,
                 char_hidden_size,
                 dropout=0.0):
        super(CharEmbed, self).__init__()

        self._char_hidden_size = char_hidden_size

        self.char_embedding = nn.Embedding(num_embeddings=char_vocab_size,
                                           embedding_dim=char_embedding_dim,
                                           padding_idx=0)
        # xavier glorot: 使用标准差为1/√n的正态分布进行初始化, n为前一层的节点数
        # 在激活函数是tanh和sigmoid时推荐使用
        nn.init.xavier_uniform_(self.char_embedding.weight, gain=nn.init.calculate_gain('relu'))
        # nn.init.xavier_uniform_(self.char_embedding.weight, gain=nn.init.calculate_gain('leaky_relu'))

        # Kaiming He：使用标准差为2/√n的正态分布进行初始化, n为前一层的节点数
        # 激活函数是Relu时推荐使用
        # nn.init.kaiming_uniform_(self.char_embedding.weight,
        #                          a=0,  # 该层后面一层的激活函数中负的斜率(默认为ReLU，此时a=0)
        #                          mode='fan_in',  # 'fan_in'(default)或'fan_out'使用fan_in保持weights的方差在前向传播中不变,使用fan_out保持weights的方差在反向传播中不变
        #                          nonlinearity='relu')

        # uniform
        # nn.init.uniform_(self.char_embedding.weight.data, -0.32, 0.32)
        # self.char_embedding.weight.data.uniform_(-0.32, 0.32)

        # self.rnn_encoder = RNNEncoder(input_size=char_hidden_size,
        #                               hidden_size=char_hidden_size,
        #                               batch_first=True,
        #                               rnn_type='gru')

        self._win_sizes = [2, 3, 4]
        self.convs = nn.ModuleList([
            nn.Sequential(
                nn.Conv1d(in_channels=char_embedding_dim,  # 输入特征维度(词向量维度)
                          out_channels=w * 25,  # 输出特征维度(卷积核个数)
                          padding=1,
                          kernel_size=w),
                nn.ReLU(),
                nn.AdaptiveMaxPool1d(1)
                # nn.AdaptiveAvgPool1d(1)
            ) for w in self._win_sizes])

        self.embed_dropout = nn.Dropout(dropout)
        self.linear_dropout = nn.Dropout(dropout)

        # 控制门
        self.gate_linear = nn.Linear(in_features=sum(self._win_sizes) * 25,
                                     out_features=char_hidden_size)
        # 门控制的偏置值尽量赋值为负数(保证初始化操作对carry起作用)
        nn.init.constant_(self.gate_linear.bias.data, -2)
        self.trans_linear = nn.Linear(in_features=sum(self._win_sizes) * 25,
                                      out_features=char_hidden_size)
        # 线性层转换，保持维度一致
        self.linear = nn.Linear(in_features=sum(self._win_sizes) * 25,
                                out_features=char_hidden_size)

        # self.dense = nn.Sequential(
        #     nn.Linear(in_features=char_hidden_size * len(self._win_sizes),
        #               out_features=char_hidden_size * len(self._win_sizes) // 2),
        #     nn.ReLU(),
        #     nn.Linear(in_features=char_hidden_size * len(self._win_sizes) // 2, out_features=char_hidden_size)
        # )

    def forward(self, chars_input):
        batch_size, wd_seq_len, char_seq_len = chars_input.size()
        # [batch, wd_seq_len, char_seq_len] -> [batch * wd_seq_len, char_seq_len]
        chars_input = chars_input.reshape(-1, char_seq_len)
        # [batch * wd_seq_len, char_seq_len] -> [batch * wd_seq_len, char_seq_len, char_embed_dim]
        char_embed = self.char_embedding(chars_input)
        # [batch * wd_seq_len, char_embed_dim, char_seq_len]
        char_embed.transpose_(1, 2)

        if self.training:
            char_embed = self.embed_dropout(char_embed)

        # [batch * wd_seq_len, char_embed_dim, 1]
        # -> [batch * wd_seq_len, char_embed_dim*3, 1]
        # -> [batch * wd_seq_len, char_embed_dim*3]
        conv_out = [conv(char_embed) for conv in self.convs]
        conv_out = torch.cat(tuple(conv_out), dim=1).squeeze(2)

        if self.training:
            conv_out = self.linear_dropout(conv_out)

        # [batch * wd_seq_len, char_embed_dim*3]
        # -> [batch * wd_seq_len, char_hidden_size] -> [batch, wd_seq_len, char_hidden_size]
        # out = self.linear(conv_out)  # [batch * wd_seq_len, char_hidden_size]
        # # out = self.dense(conv_out)
        # out = out.reshape(batch_size, wd_seq_len, -1)  # [batch, wd_seq_len, char_hidden_size]

        # Highway network
        gate_out = self.gate_linear(conv_out).reshape(batch_size, wd_seq_len, -1)
        transform_gate = torch.sigmoid(gate_out)  # [batch, wd_seq_len, char_hidden_size]
        carry_gate = 1. - transform_gate  # [batch, wd_seq_len, char_hidden_size]

        trans_out = self.trans_linear(conv_out).reshape(batch_size, wd_seq_len, -1)
        allow_trans = torch.mul(transform_gate, F.relu(trans_out))  # [batch, wd_seq_len, char_hidden_size]
        # 保证维度一致：1、线性变换  2、zero-padding  3、sub-sampling
        # zeros_pad = torch.zeros(batch_size, wd_seq_len, (conv_out.size(2) - self._char_hidden_size))
        # carry_out = self.linear(conv_out).reshape((batch_size, wd_seq_len, -1))  # 线性变换
        out = conv_out.reshape((batch_size, wd_seq_len, -1))
        carry_out = out[:, :, :self._char_hidden_size]  # sub-sampling

        allow_carry = torch.mul(carry_gate, carry_out)

        allow_out = torch.add(allow_trans, allow_carry)
        return allow_out
