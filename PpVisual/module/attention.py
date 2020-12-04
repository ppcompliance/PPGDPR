import torch.nn.functional as F

from module.layers import *


class Attention(nn.Module):
    def __init__(self, hidden, dropout_mlp):
        super(Attention, self).__init__()
        # hidden = 2 * lstm_hidden
        self.dropout_mlp = dropout_mlp
        self.weight = nn.Parameter(torch.Tensor(hidden, hidden))
        W = orthonormal_initializer(hidden, hidden)
        self.weight.data.copy_(torch.from_numpy(W))

        self.bias = nn.Parameter(torch.Tensor(hidden))
        b = np.zeros(hidden, dtype=np.float32)
        self.bias.data.copy_(torch.from_numpy(b))

        self.query = nn.Parameter(torch.Tensor(hidden))
        self.query.data.normal_(mean=0.0, std=0.05)

    def forward(self, batch_hidden, batch_masks):
        # batch_hidden: b x len x hidden (2 * lstm_hidden)
        # batch_masks:  b x len
        batch_size = batch_hidden.shape[0]
        length = batch_hidden.shape[1]

        if self.training:
            batch_hidden = drop_sequence_sharedmask(batch_hidden, self.dropout_mlp)

        # linear
        key = torch.matmul(batch_hidden, self.weight) + self.bias  # b x len x hidden

        if self.training:
            key = drop_sequence_sharedmask(key, self.dropout_mlp)

        # compute attention
        outputs = torch.matmul(key, self.query)  # b x len

        masked_outputs = outputs.masked_fill((1 - batch_masks).bool(), float(-1e32))

        attn_scores = F.softmax(masked_outputs, dim=1)  # b x len
        # 对于全零向量，-1e32的结果为 1/len, -inf为nan, 额外补0
        masked_attn_scores = attn_scores.masked_fill((1 - batch_masks).bool(), 0.0)

        # sum weighted sources
        batch_outputs = torch.bmm(masked_attn_scores.unsqueeze(1), key).squeeze(1)  # b x hidden

        return batch_outputs, attn_scores
