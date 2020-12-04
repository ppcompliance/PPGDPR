import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn


class KMaxPool1d(nn.Module):  # 提取k个最大值并保持相对顺序不变
    def __init__(self, top_k):
        super(KMaxPool1d, self).__init__()
        self.top_k = top_k

    def forward(self, inputs):
        assert torch.is_tensor(inputs) and inputs.dim() == 3
        # 注: torch.topk和torch.sort均返回的是：values, indices
        rand_top_idxs = torch.topk(inputs, k=self.top_k, dim=2)[1]
        top_idxs = rand_top_idxs.sort(dim=2)[0]
        # gather: 沿给定轴dim, 将输入索引张量index指定位置的值进行聚合(抽取)
        return inputs.gather(dim=2, index=top_idxs)


class TexCNN(nn.Module):
    def __init__(self, args, embedding_weights):
        super(TexCNN, self).__init__()

        embedding_dim = embedding_weights.shape[1]
        print('embedding_dim:', embedding_dim)
        self.vecword_embedding = nn.Embedding.from_pretrained(torch.from_numpy(embedding_weights))
        self.vecword_embedding.weight.requires_grad = False

        self.word_embedding = nn.Embedding(num_embeddings=args.vocab_size,  # 词表大小
                                           embedding_dim=embedding_dim)  # 词向量维度
        init_weights = torch.zeros(args.vocab_size, embedding_dim, dtype=torch.float32, device=args.device)
        self.word_embedding.weight = nn.Parameter(init_weights)
        # self.word_embedding.weight.data.copy_(init_weights)
        # self.word_embedding.weight.requires_grad = True

        # 卷积 -> ReLU激活 -> 池化
        # conv_out = ceil((conv_in + 2 * padding - win_size) / stride) + 1
        self.win_size = 3
        # 类似于做3-gram, 4-gram, 5-gram来提取语义特征,
        # 每一个卷积核对应的特征不同
        self.win_sizes = [3, 4, 5]
        self.padding = 1
        # self.max_seq_len = 100
        # self.conv_out = (self.max_seq_len + 2 * self.padding - self.win_size) + 1
        # self.conv = nn.Sequential(
        #                 nn.Conv1d(in_channels=embedding_dim,  # 输入数据的特征维度(词向量维度)
        #                    out_channels=args.hidden_size, # 卷积输出的特征维度(卷积核个数)
        #                    padding=self.padding,
        #                    kernel_size=self.win_size),
        #                 nn.ReLU(),
        #                 nn.MaxPool1d(kernel_size=self.conv_out)
        #                 # nn.AdaptiveMaxPool1d(1)
        #             )

        # self.conv_1d = nn.Conv1d(in_channels=embedding_dim,
        #                          out_channels=args.hidden_size,
        #                          padding=self.padding,
        #                          kernel_size=self.win_size)

        self.convs = nn.ModuleList([
                        nn.Sequential(
                            nn.Conv1d(in_channels=embedding_dim,  # 输入数据的特征维度(词向量维度)
                                      out_channels=25 * w,  # 卷积输出的特征维度(卷积核个数)
                                      padding=self.padding,
                                      kernel_size=w),
                            nn.ReLU(),
                            nn.AdaptiveMaxPool1d(1)
                            # KMaxPool1d(2)
                        ) for w in self.win_sizes])

        self.embed_dropout = nn.Dropout(args.embed_dropout)
        self.linear_dropout = nn.Dropout(args.linear_dropout)

        self.linear = nn.Linear(in_features=25 * sum(self.win_sizes),
                                out_features=args.label_size)

        # self.linear = nn.Sequential(
        #     nn.Linear(args.hidden_size * len(self.win_sizes), args.hidden_size),
        #     nn.Dropout(args.linear_dropout),
        #     nn.ReLU(),
        #     nn.Linear(args.hidden_size, args.label_size)
        # )

    def forward(self, wd_ids, vecwd_ids):  # [batch_size, max_seq_len]
        # 词索引 -> 词向量(embedding)
        wd_embed = self.word_embedding(wd_ids)  # [batch_size, max_seq_len, embedding_dim]
        vecwd_embed = self.vecword_embedding(vecwd_ids)  # [batch_size, max_seq_len, embedding_dim]
        embed = wd_embed + vecwd_embed  # [batch_size, max_seq_len, embedding_dim]

        # Dropout
        if self.training:
            embed = self.embed_dropout(embed)

        conv_in = embed.transpose(1, 2)  # [batch_size, embedding_dim, max_seq_len]

        # 卷积层 -> ReLu -> 池化层
        # conv_out = self.conv_1d(conv_in)  # [batch_size, hidden_size, conv_out]
        # # [batch_size, hidden_size, 1] ->   # [batch_size, hidden_size]
        # out = F.max_pool1d(F.relu(conv_out), kernel_size=conv_out.size(2)).squeeze(2)

        conv_out = [conv(conv_in) for conv in self.convs]
        # [batch_size, hidden_size, 1] -> [batch_size, hidden_size * 3]
        out = torch.cat(tuple(conv_out), dim=1).squeeze(2)

        # conv_out = [conv(conv_in) for conv in self.convs]
        # conv_out = [co.reshape(co.shape[0], -1) for co in conv_out]
        # out = torch.cat(tuple(conv_out), dim=1)

        # Dropout
        if self.training:
            out = self.linear_dropout(out)

        # 全连接层(dropout)
        out = self.linear(out)

        return out
