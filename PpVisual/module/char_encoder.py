import torch
import torch.nn as nn
from .rnn_cell import RNNNet

'''
字符级别的特征提取:
char id -> CNN -> Dense -> BiLSTM -> Dense -> class
CNN: n-gram特征提取
'''


class CharEncoder(nn.Module):
    def __init__(self):
        super(CharEncoder, self).__init__()

        self.char_embedding = nn.Embedding(num_embeddings=2000,  # 字符表的大小
                                           embedding_dim=100,  # 字符向量的维度
                                           padding_idx=0)    # 0索引的向量置0
        nn.init.xavier_uniform_(self.char_embedding.weight, gain=nn.init.calculate_gain('relu'))
        # nn.init.uniform_(self.char_embedding.weight.data, -0.32, 0.32)

        self._win_sizes = [3, 4, 5]
        self._cnn_encoder = nn.ModuleList([
            nn.Sequential(
                nn.Conv1d(in_channels=100,  # 字符向量维度
                          out_channels=50,  # 卷积输出的特征维度
                          kernel_size=w),
                nn.ReLU(),
                nn.AdaptiveMaxPool1d(1)
            ) for w in self._win_sizes
        ])

        # 使卷积提取的特征更加稠密
        self.cnn_dense = nn.Linear(in_features=50 * len(self._win_sizes),
                                   out_features=150)

        self.bilstm = RNNNet(input_size=150,
                             hidden_size=200,
                             nb_layer=1,
                             dropout=0.0,
                             batch_first=True,
                             bidirectional=True)

        # 分类
        self.dense = nn.Sequential(
            nn.Linear(200, 100),
            nn.ReLU(),
            nn.Linear(100, 3)
        )

    def forward(self, *input):
        pass

