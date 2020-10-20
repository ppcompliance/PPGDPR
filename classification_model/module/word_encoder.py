import logging

from module.encoder import Encoder
from module.layers import *

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class WordEncoder(Encoder):
    def __init__(self, config, vocab):
        super(WordEncoder, self).__init__(config.dropout_mlp)
        self.dropout_embed = config.dropout_embed

        word_embed = np.zeros((vocab.word_size, config.word_dims), dtype=np.float32)
        self.word_embed = nn.Embedding(vocab.word_size, config.word_dims, padding_idx=0)
        self.word_embed.weight.data.copy_(torch.from_numpy(word_embed))

        extword_embed = vocab.load_pretrained_embs(config.glove_path)
        extword_size, word_dims = extword_embed.shape
        logging.info("Load extword embed: words %d, dims %d." % (extword_size, word_dims))

        self.extword_embed = nn.Embedding(extword_size, word_dims, padding_idx=0)
        self.extword_embed.weight.data.copy_(torch.from_numpy(extword_embed))
        self.extword_embed.weight.requires_grad = False

        input_size = config.word_dims

        self.word_lstm = LSTM(
            input_size=input_size,
            hidden_size=config.word_hidden_size,
            num_layers=config.word_num_layers,
            batch_first=True,
            bidirectional=True,
            dropout_in=config.dropout_input,
            dropout_out=config.dropout_hidden,
        )

    def forward(self, word_inputs):
        # batch_inputs1 word: sen_num x sent_len
        # batch_inputs2 extword: sen_num x sent_len
        # weights       sen_num x sent_len
        # batch_masks   sen_num x sent_len

        batch_inputs1, batch_inputs2, batch_masks = word_inputs

        batch_embed1 = self.word_embed(batch_inputs1)  # sen_num x sent_len x 100
        batch_embed2 = self.extword_embed(batch_inputs2)

        batch_embed = batch_embed1 + batch_embed2

        if self.training:
            batch_embed = drop_input_independent(batch_embed, self.dropout_embed)

        assert torch.all(torch.sum(batch_masks, 1) > 0), "sent len should > 0."

        hiddens, _ = self.word_lstm(batch_embed, batch_masks, initial=None)  # sent_len x sen_num x hidden*2
        hiddens.transpose_(1, 0)  # sen_num x sent_len x hidden*2

        reps = self.last_pooling(hiddens, batch_masks)

        if self.training:
            reps = self.dropout(reps)

        outputs = self.out(reps)

        return outputs
