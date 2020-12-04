import torch
import torch.nn as nn
import torch.nn.functional as F
import math

'''注意力机制'''


# ∑softmax(W*tanh(V*h))
class SelfAttention(nn.Module):
    def __init__(self, hidden_size):
        super(SelfAttention, self).__init__()
        self.relation = nn.Sequential(
            nn.Linear(hidden_size, hidden_size//2),
            nn.ReLU(),  # nn.Tanh
            nn.Linear(hidden_size//2, 1)
        )

    def forward(self, encoder_output):
        # [batch_size, seq_len, hidden_size]
        # -> [batch_size, seq_len, 1]
        rout = self.relation(encoder_output)
        # [batch_size, seq_len, 1] -> [batch_size, seq_len]
        weights = F.softmax(rout.squeeze(2), dim=1)
        # [batch_size, seq_len, hidden_size] * [batch_size, seq_len, 1]
        # -> [batch_size, seq_len, hidden_size] -> [batch_size, hidden_size]
        out = (encoder_output * weights.unsqueeze(-1)).sum(dim=1)
        # [batch_size, hidden_size]
        out = torch.tanh(out)

        return out, weights


# attention
# att(Q, K, V) = ∑softmax(Q'K/√dim_k)V
class Attention(nn.Module):
    def __init__(self):
        super(Attention, self).__init__()
        pass

    def forward(self, query, keys, values):
        '''
        :param query: [batch_size, Q]
        :param keys: [batch_size, seq_len, K]
        :param values: [batch_size, seq_len, V]
        more: K==Q  keys==values(K==V)
        :return: out:[batch_size, V]  weights:[batch_size, seq_len]
        '''
        # 调节因子，防止内积过大
        scale = 1. / math.sqrt(keys.size(2))

        # [batch_size, 1, Q] * [batch_size, K, seq_len] ->
        # [batch_size, 1, seq_len] -> [batch_size, seq_len]
        att_weights = torch.bmm(query.unsqueeze(1), keys.transpose(1, 2)).squeeze(1)
        # [batch_size, seq_len]
        soft_att_weights = F.softmax(att_weights.mul(scale), dim=1)
        # [batch_size, 1, seq_len] * [batch_size, seq_len, V] -> [batch_size, V]
        att_out = torch.bmm(soft_att_weights.unsqueeze(1), values).squeeze(1)

        # # [batch_size, seq_len, K] * [batch_size, Q, 1] ->
        # # [batch_size, seq_len, 1] -> [batch_size, seq_len]
        # att_weights = torch.bmm(keys, query.unsqueeze(2)).squeeze(2)
        # # [batch_size, seq_len]
        # soft_att_weights = F.softmax(att_weights.mul(scale), dim=1)
        # # [batch_size, V, seq_len] * [batch_size, seq_len, 1] -> [batch_size, V, 1]
        # att_out = torch.bmm(values.transpose(1, 2), soft_att_weights.unsqueeze(2)).squeeze(2)
        # print(soft_att_weights.size())
        return att_out, soft_att_weights


if __name__ == '__main__':
    k = torch.rand((3, 10, 50))
    v = k
    q = torch.rand((3, 50))
    att = Attention()
    y, w = att(q, k, v)


