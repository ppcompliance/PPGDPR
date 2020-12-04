from module.layers import *


class SentEncoder(nn.Module):
    """LSTM encoder."""

    def __init__(self, config):
        super(SentEncoder, self).__init__()
        self.lstm = LSTM(
            input_size=config.word_hidden_size * 2,
            hidden_size=config.sent_hidden_size,
            num_layers=config.sent_num_layers,
            batch_first=True,
            bidirectional=True,
            dropout_in=config.dropout_input,
            dropout_out=config.dropout_hidden,
        )

    def forward(self, sent_reps, sent_masks):
        # sent_reps:  b x doc_len x sent_rep_size
        # sent_masks: b x doc_len

        sent_hiddens, _ = self.lstm(sent_reps, sent_masks, initial=None)  # doc_len x b x hidden*2
        sent_hiddens = sent_hiddens.transpose(1, 0)  # b x doc_len x hidden*2

        return sent_hiddens
