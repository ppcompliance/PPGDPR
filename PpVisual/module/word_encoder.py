import logging

from module.layers import *

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class WordEncoder(nn.Module):
    """LSTM encoder."""

    def __init__(self, config, vocab):
        super(WordEncoder, self).__init__()
        self.dropout_embed = config.dropout_embed

        word_embed = np.zeros((vocab.word_size, config.word_dims), dtype=np.float32)
        self.word_embed = nn.Embedding(vocab.word_size, config.word_dims, padding_idx=0)
        self.word_embed.weight.data.copy_(torch.from_numpy(word_embed))

        extword_embed = vocab.load_pretrained_embs(config.glove_path)
        self.extword_embed = nn.Embedding(vocab.extword_size, config.word_dims, padding_idx=0)
        self.extword_embed.weight.data.copy_(torch.from_numpy(extword_embed))
        self.extword_embed.weight.requires_grad = False

        self.lstm = LSTM(
            input_size=config.word_dims,
            hidden_size=config.word_hidden_size,
            num_layers=config.word_num_layers,
            batch_first=True,
            bidirectional=True,
            dropout_in=config.dropout_input,
            dropout_out=config.dropout_hidden,
        )

    def forward(self, batch_inputs1, batch_inputs2, batch_masks):
        # batch_inputs1 word: sen_num x sent_len
        # batch_inputs2 extword: sen_num x sent_len
        # batch_masks: sen_num x sent_len

        batch_embed1 = self.word_embed(batch_inputs1)  # sen_num x sent_len x 100
        batch_embed2 = self.extword_embed(batch_inputs2)  # sen_num x sent_len x 100
        batch_embed = batch_embed1 + batch_embed2
        # batch_embed = batch_embed2


        if self.training:
            batch_embed = drop_input_independent(batch_embed, self.dropout_embed)

        batch_hiddens, _ = self.lstm(batch_embed, batch_masks, initial=None)  # sent_len x sen_num x hidden*2
        batch_hiddens = batch_hiddens.transpose(1, 0)  # sen_num x sent_len x hidden*2

        return batch_hiddens
