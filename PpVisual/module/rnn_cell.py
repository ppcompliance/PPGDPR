import torch
import torch.nn as nn

'''
采用RNNCell、LSTMCell、GRUCell重构RNN、LSTM和GRU模型，解决序列对齐问题并做灵活扩充

LSTMCell  (input_size, hidden_size, bias=True)
    输入: input, (h_0, c_0)
        input (seq_len, batch, input_size): 包含输入序列特征的Tensor。也可以是packed variable
        h_0 (batch, hidden_size): 保存着batch中每个元素的初始化隐状态的Tensor
        c_0 (batch, hidden_size): 保存着batch中每个元素的初始化细胞状态的Tensor
    
    输出：h_1, c_1
        h_1 (batch, hidden_size): 下一个时刻的隐状态。
        c_1 (batch, hidden_size): 下一个时刻的细胞状态。

GRUCell  (input_size, hidden_size, bias=True)
    输入: input, h0
        input (batch, input_size): 包含输入序列特征的Tensor。也可以是packed variable
        h_0 (batch, hidden_size): 保存着batch中每个元素的初始化隐状态的Tensor
        c_0 (batch, hidden_size): 保存着batch中每个元素的初始化细胞状态的Tensor
    
    输出：h_1
        h_1 (batch, hidden_size): 下一个时刻的隐状态。
        c_1 (batch, hidden_size): 下一个时刻的细胞状态。
        
        
LSTM  (input_size, hidden_size, num_layers, batch_first, dropout, bidirectional)
输入: input, (h_0, c_0)
    input (seq_len, batch, input_size): 包含输入序列特征的Tensor。也可以是packed variable ，详见 [pack_padded_sequence](#torch.nn.utils.rnn.pack_padded_sequence(input, lengths, batch_first=False[source])
    h_0 (num_layers * num_directions, batch, hidden_size):保存着batch中每个元素的初始化隐状态的Tensor
    c_0 (num_layers * num_directions, batch, hidden_size): 保存着batch中每个元素的初始化细胞状态的Tensor

输出: output, (h_n, c_n)
    output (seq_len, batch, hidden_size * num_directions): 保存RNN最后一层的输出的Tensor。 如果输入是torch.nn.utils.rnn.PackedSequence，那么输出也是torch.nn.utils.rnn.PackedSequence。
    h_n (num_layers * num_directions, batch, hidden_size): Tensor，保存着RNN最后一个时间步的隐状态。
    c_n (num_layers * num_directions, batch, hidden_size): Tensor，保存着RNN最后一个时间步的细胞状态。
    
GRU  (input_size, hidden_size, num_layers, batch_first, dropout, bidirectional)
输入: input, h_0
    input (seq_len, batch, input_size): 包含输入序列特征的Tensor。也可以是packed variable ，详见 [pack_padded_sequence](#torch.nn.utils.rnn.pack_padded_sequence(input, lengths, batch_first=False[source])
    h_0 (num_layers * num_directions, batch, hidden_size):保存着batch中每个元素的初始化隐状态的Tensor

输出: output, h_n
    output (seq_len, batch, hidden_size * num_directions): 保存RNN最后一层的输出的Tensor。 如果输入是torch.nn.utils.rnn.PackedSequence，那么输出也是torch.nn.utils.rnn.PackedSequence。
    h_n (num_layers * num_directions, batch, hidden_size): Tensor，保存着RNN最后一个时间步的隐状态。
'''

class RNNNet(nn.Module):
    def __init__(self, input_size,  # 输入数据的特征维度(可变)
                 hidden_size,  # 隐层状态的特征维度
                 nb_layer=1,  # 层数
                 dropout=0.0,
                 batch_first=False,
                 bidirectional=False,
                 rnn_type='lstm'):
        super(RNNNet, self).__init__()

        self._hidden_size = hidden_size
        self._nb_layer = nb_layer
        self._batch_first = batch_first
        self._dropout = dropout
        self._bidirectional = bidirectional
        self._nb_directions = 2 if bidirectional else 1

        self._rnn_type = rnn_type.upper()
        self._rnn_types = ['RNN', 'GRU', 'LSTM']
        assert self._rnn_type in self._rnn_types
        # 获得相应的RNN单元构造方法
        self._rnn_cell = getattr(nn, self._rnn_type+'Cell')

        # 根据层数纵向扩展节点
        self._fw_cells = nn.ModuleList()
        self._bw_cells = nn.ModuleList()
        for layer_i in range(self._nb_layer):
            layer_input_size = input_size if layer_i == 0 else self._nb_directions * self._hidden_size
            self._fw_cells.append(self._rnn_cell(input_size=layer_input_size,
                                                 hidden_size=self._hidden_size))
            if self._bidirectional:
                self._bw_cells.append(self._rnn_cell(input_size=layer_input_size,
                                                     hidden_size=self._hidden_size))

    def _forward(self, cell, inputs, mask, init_hidden):
        # inputs: [seq_len, batch, input_size]
        # init_hidden: [batch, hidden_size]
        # mask: [seq_len, batch, hidden_size]
        seq_len = inputs.size(0)
        outputs = []
        hx_fw = init_hidden
        for xi in range(seq_len):  # 根据序列长度横向扩展
            if self._rnn_type == 'LSTM':
                # inputs[xi]: [batch, input_size]
                # hx_fw: [batch, hidden_size]
                # h_next c_next: [batch, hidden_size]
                # mask[xi]: [batch, hidden_size]
                h_next, c_next = cell(inputs[xi], hx_fw)
                h_next = h_next * mask[xi] + init_hidden[0] * (1 - mask[xi])  # 点乘
                c_next = c_next * mask[xi] + init_hidden[1] * (1 - mask[xi])

                outputs.append(h_next)

                hx_fw = (h_next, c_next)
            else:
                h_next = cell(inputs[xi], hx_fw)
                h_next = h_next * mask[xi] + init_hidden * (1 - mask[xi])

                outputs.append(h_next)

                hx_fw = h_next

        # [seq_len, batch, hidden_size]
        out = torch.stack(tuple(outputs), dim=0)
        return out, hx_fw

    def _backward(self, cell, inputs, mask, init_hidden):
        # inputs: [seq_len, batch, input_size]
        # init_hidden: [batch, hidden_size]
        seq_len = inputs.size(0)
        hx_bw = init_hidden
        outputs = []

        for xi in reversed(range(seq_len)):  # 逆向取值
            if self._rnn_type == 'LSTM':
                h_next, c_next = cell(inputs[xi], hx_bw)
                h_next = h_next * mask[xi] + init_hidden[0] * (1 - mask[xi])
                c_next = c_next * mask[xi] + init_hidden[1] * (1 - mask[xi])

                outputs.append(h_next)

                hx_bw = (h_next, c_next)

            else:
                h_next = cell(inputs[xi], hx_bw)
                h_next = h_next * mask[xi] + init_hidden * (1 - mask[xi])

                outputs.append(h_next)

                hx_bw = h_next

        outputs.reverse()
        out = torch.stack(tuple(outputs), dim=0)
        return out, hx_bw

    def _init_hidden(self, batch_size, device=torch.device('cpu')):
        hn = torch.randn(batch_size, self._hidden_size, device=device)
        return (hn, hn) if self._rnn_type == 'LSTM' else hn

    def _drop_out(self, inputs, p=0.5, training=True):
        if training:
            assert inputs.dim() == 2 or inputs.dim() == 3
            if inputs.dim() == 2:
                # inputs: [batch_size, hidden_size]
                # 每个节点有p的概率被置成0，1-p的概率被置成1
                drop_mask = torch.zeros(inputs.shape, device=inputs.device).fill_(1-p)
                # 输入中所有值必须在[0, 1]区间，输出张量的第i个元素值，将以输入张量的第i个概率值等于1
                drop_mask = torch.bernoulli(drop_mask)
                inputs.mul_(drop_mask.div(1-p))
            else:
                # inputs: [seq_len, batch_size, input_size]
                drop_mask = torch.zeros(inputs.shape[1], inputs.shape[2], device=inputs.device).fill_(1-p)
                drop_mask = torch.bernoulli(drop_mask)
                drop_mask.div_(1 - p)
                drop_mask = drop_mask.unsqueeze(-1).expand((-1, -1, inputs.shape[0])).permute((2, 0, 1))
                inputs.mul_(drop_mask)
        return inputs

    def forward(self, inputs, mask):
        if self._batch_first:  # [batch_size, seq_len, input_size]
            inputs.transpose_(0, 1)  # [ seq_len, batch_size, input_size]
            mask.transpose_(0, 1)  # [seq_len, batch_size]

        # [seq_len, batch_size] -> [seq_len, batch_size, 1] -> [seq_len, batch_size, hidden_size]
        mask = mask.unsqueeze(-1).expand((-1, -1, self._hidden_size))

        init_hidden = self._init_hidden(inputs.size(1), inputs.device)

        fw_out, bw_out = None, None
        fw_hidden, bw_hidden = None, None
        hn, cn = [], []
        for i in range(self._nb_layer):
            if i != 0:
                inputs = self._drop_out(inputs, p=0.4, training=self.training)

            fw_out, fw_hidden = self._forward(self._fw_cells[i], inputs, mask, init_hidden)
            if self._bidirectional:
                bw_out, bw_hidden = self._backward(self._bw_cells[i], inputs, mask, init_hidden)

            if self._rnn_type == 'LSTM':
                hn.append(torch.cat((fw_hidden[0], bw_hidden[0]), dim=1) if self._bidirectional else fw_hidden[0])
                cn.append(torch.cat((fw_hidden[1], bw_hidden[1]), dim=1) if self._bidirectional else fw_hidden[1])
            else:
                hn.append(torch.cat((fw_hidden, bw_hidden), dim=1) if self._bidirectional else fw_hidden)

            # [seq_len, batch, hidden_size] -> [seq_len, batch, hidden_size * 2]
            inputs = torch.cat((fw_out, bw_out), dim=2) if self._bidirectional else fw_out

        out = inputs.transpose(0, 1) if self._batch_first else inputs

        if self._bidirectional:
            hidden = (torch.stack(tuple(hn), dim=0), torch.stack(tuple(cn), dim=0))
        else:
            hidden = torch.stack(tuple(hn), dim=0)

        return out, hidden
