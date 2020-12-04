import subprocess
import time
import json
import os
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

from src.loader import *
from src.optimizer import Optimizer

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s: %(message)s')


class Trainer():
    def __init__(self, model, config, vocab, att_out=False, save_model = None):
        self.model = model
        self.config = config
        self.epoch_num = int(config.epoch_num)
        self.writer = SummaryWriter(log_dir=config.log_dir)

        self.train_data = getExamples(self.config.train_file, model.word_encoder, vocab)
        self.batch_num = int(np.ceil(len(self.train_data) / float(self.config.train_batch_size)))

        self.dev_data = getExamples(self.config.dev_file, model.word_encoder, vocab)
        self.test_data = getTestExamples(config.test_data, model.word_encoder, vocab)
        self.label = ['Policy_Introductory', 'First_Party_Collection_and_Use', 'Cookies_and_Similar_Technologies', 'Third_Party_Share_and_Collection',
        'User_Right_and_Control','Data_Security', 'Data_Retention', 'International_Data_Transfer', 'Specific_Audiences',
        'Policy_Change', 'Policy_Contact_Information']
        self.label = [i.lower() for i in self.label]
        self.convert_label = [self.label.index(i) for i in vocab.id2label]

        # criterion
        weight = torch.FloatTensor(vocab.label_weights)
        if config.use_cuda:
            weight = weight.to(config.device)
        self.criterion = nn.CrossEntropyLoss(weight)
        # optimizer
        self.optimizer = Optimizer(model.parameters, config, self.batch_num)
        self.att_out = att_out
        if self.att_out:
            self.config.save_model = save_model

    def train(self):
        assert self.att_out == False
        self.step = 0
        self.early_stop = -1
        self.best_train_acc, self.best_dev_acc, self.best_test_acc = 0, 0, 0

        # self.model = nn.DataParallel(self.model)

        for epoch in range(1, self.config.epochs):
            train_acc = self._train(epoch)
            # self.logging_gpu_memory()
            dev_acc = self._eval(epoch, "dev")
            # self.logging_gpu_memory()
            test_acc = self._eval(epoch, "test")
            # self.logging_gpu_memory()

            # with open('test_result/test_result_'+self.config.fold+'.txt', "a+", encoding='utf8') as f:
            #     f.write(str(test_acc) + '\n')
            if int(self.epoch_num) <= 0:
                if self.best_dev_acc < dev_acc:
                    logging.info("Exceed history dev acc = %.2f, current = %.2f" % (self.best_dev_acc, dev_acc))
                    if epoch > self.config.save_after:
                        torch.save(self.model.state_dict(), self.config.save_model)

                    self.best_train_acc = train_acc
                    self.best_dev_acc = dev_acc
                    self.best_test_acc = test_acc
                    self.early_stop = 0
                else:
                    self.early_stop += 1
                    if self.early_stop == self.config.early_stops:
                        logging.info(
                            "Eearly stop in epoch %d, best train_acc: %.2f, dev_acc: %.2f, test acc: %.2f " % (
                                epoch - self.config.early_stops, self.best_train_acc, self.best_dev_acc,
                                self.best_test_acc))
                        break
            else:
                if self.best_dev_acc < dev_acc:
                    logging.info("Exceed history dev acc = %.2f, current = %.2f" % (self.best_dev_acc, dev_acc))
                    self.best_train_acc = train_acc
                    self.best_dev_acc = dev_acc
                    self.best_test_acc = test_acc
                if int(epoch) >= self.epoch_num:
                    torch.save(self.model.state_dict(), self.config.save_model)
                    break

    def test(self):
        self.model.load_state_dict(torch.load(self.config.save_model))
        test_batch_size = self.config.test_batch_size
        test_batch_size = 2 * test_batch_size if test_batch_size == 1 else test_batch_size // 2
        test_acc = self._eval(-1, "test", test_batch_size=test_batch_size)
        if test_acc != self.best_test_acc:
            logging.info('Serious bug: Test acc is different.')

    def att_test(self):
        self.model.load_state_dict(torch.load(DIR+self.config.save_model))
        test_batch_size = self.config.test_batch_size
        # test_batch_size = 2 * test_batch_size if test_batch_size == 1 else test_batch_size // 2
        test_acc, label_pred, w_att_result, s_att_result = self._att_eval(-1, "test", test_batch_size=test_batch_size)
        return label_pred, w_att_result, s_att_result
        # if test_acc != self.best_test_acc:
        #     logging.info('Serious bug: Test acc is different.')

    def _train(self, epoch):
        self.optimizer.zero_grad()
        self.model.train()

        start_time = time.time()
        epoch_start_time = time.time()
        overall_corrects, overall_totals, overall_losses = 0, 0, 0
        corrects, totals, losses = 0, 0, 0
        batch_idx = 1
        for batch_data in data_iter(self.train_data, self.config.train_batch_size, True):
            torch.cuda.empty_cache()
            batch_inputs, batch_masks, batch_labels = self.batch2tensor(batch_data)
            # p = self.model.named_parameters()

            batch_outputs = self.model(batch_inputs, batch_masks)

            loss = self.criterion(batch_outputs, batch_labels)
            loss = loss / self.config.update_every
            loss_value = loss.detach().cpu().item()
            losses += loss_value
            overall_losses += loss_value
            loss.backward()

            correct = sum((torch.max(batch_outputs, dim=1)[1] == batch_labels).cpu().numpy())
            total = batch_labels.shape[0]

            corrects += correct
            totals += total

            overall_corrects += correct
            overall_totals += total

            if batch_idx % self.config.update_every == 0 or batch_idx == self.batch_num:
                nn.utils.clip_grad_norm_(self.optimizer.all_params, max_norm=self.config.clip)
                for optimizer, scheduler in zip(self.optimizer.optims, self.optimizer.schedulers):
                    optimizer.step()
                    scheduler.step()
                self.optimizer.zero_grad()

                self.step += 1

            if batch_idx % self.config.log_interval == 0:
                elapsed = time.time() - start_time
                acc = corrects * 100.0 / totals

                lrs = self.optimizer.get_lr()
                logging.info(
                    '| epoch {:3d} | step {:3d} | batch {:3d}/{:3d} | lr{} | acc {:.2f} | loss {:.4f} | s/batch {:.2f}'.format(
                        epoch, self.step, batch_idx, self.batch_num, lrs, acc,
                        losses / self.config.log_interval,
                        elapsed / self.config.log_interval))

                start_time = time.time()
                corrects, totals, losses = 0, 0, 0

            batch_idx += 1

        overall_acc = overall_corrects * 100.0 / overall_totals
        overall_losses /= self.batch_num
        during_time = time.time() - epoch_start_time

        self.writer.add_scalar('train/loss', overall_losses, epoch)
        self.writer.add_scalar('train/acc', overall_acc, epoch)
        logging.info(
            '| epoch {:3d} | acc {:.2f} | loss {:.2f} | time {:.2f}'.format(epoch, overall_acc, overall_losses,
                                                                            during_time))
        return overall_acc

    def _eval(self, epoch, data_nane, test_batch_size=None):
        self.model.eval()

        start_time = time.time()
        corrects, totals = 0, 0

        if data_nane == "dev":
            data = self.dev_data
        elif data_nane == "test":
            data = self.test_data
        else:
            Exception("No name data.")

        if test_batch_size is None:
            test_batch_size = self.config.test_batch_size

        if int(self.epoch_num) <= 0:
            result_writer = open("result/"+self.config.model_name+data_nane+"_result_fold_" + self.config.fold +"_e_"+str(epoch)+ ".tsv",
                                 'a', encoding="utf-8")
            result_writer.writelines("labelpredict\tlabelreal\tparagraph\n")

        with torch.no_grad():
            for batch_data in data_iter(data, test_batch_size, shuffle=False):
                torch.cuda.empty_cache()
                batch_inputs, batch_masks, batch_labels = self.batch2tensor(batch_data)
                batch_outputs = self.model(batch_inputs, batch_masks)
                _, label_pred = batch_outputs.max(1)
                for i in range(len(batch_outputs)):
                    if int(self.epoch_num) <= 0:
                        result_writer.writelines(str(int(label_pred[i])) + "\t" + str(int(batch_labels[i])) + "\t" + "none" + "\n")

                corrects += sum((torch.max(batch_outputs, dim=1)[1] == batch_labels).cpu().numpy())
                totals += batch_labels.shape[0]

            acc = corrects * 100.0 / totals
            during_time = time.time() - start_time

            self.writer.add_scalar(data_nane + '/acc', acc, epoch)
            logging.info(
                '| epoch {:3d} | {} acc {:5d}/{:5d} = {:.2f} | time {:.2f}'.format(epoch, data_nane, corrects, totals,
                                                                                   acc,
                                                                                   during_time))

        return acc

    def _att_eval(self, epoch, data_nane, test_batch_size=1):
        self.model.eval()

        start_time = time.time()
        corrects, totals = 0, 0

        if data_nane == "dev":
            data = self.dev_data
        elif data_nane == "test":
            data = self.test_data
        else:
            Exception("No name data.")

        if test_batch_size is None:
            test_batch_size = self.config.test_batch_size

        if int(self.epoch_num) <= 0:
            result_writer = open("att_label.tsv", 'a', encoding="utf-8")
            result_writer.writelines("labelpredict\tlabelreal\tparagraph\n")
        pred_result = []
        w_att_result = []
        s_att_result = []

        with torch.no_grad():
            for batch_data in data_iter(data, test_batch_size, shuffle=False):
                torch.cuda.empty_cache()
                batch_inputs, batch_masks, batch_labels = self.batch2tensor(batch_data)
                batch_outputs, w_att, s_att = self.model(batch_inputs, batch_masks)
                w_att = w_att.cpu().numpy().tolist()
                s_att = s_att.cpu().numpy().tolist()

                # with open("w_att.json", "a+", encoding="utf8") as f:
                w_att_result.append(json.dumps(w_att))
                    # f.write( + '\n')
                # with open("s_att.json", "a+", encoding="utf8") as f:
                #     f.write( + '\n')
                s_att_result.append(json.dumps(s_att[0]))
                _, label_pred = batch_outputs.max(1)
                for i in range(len(batch_outputs)):
                    if int(self.epoch_num) <= 0:

                        pred_result.append(self.convert_label[int(label_pred[i])])
                        result_writer.writelines(str(int(self.convert_label[int(label_pred[i])])) + "\t" + str(int(batch_labels[i])) + "\t" + "none" + "\n")

                corrects += sum((torch.max(batch_outputs, dim=1)[1] == batch_labels).cpu().numpy())
                totals += batch_labels.shape[0]

            acc = corrects * 100.0 / totals
            during_time = time.time() - start_time

            self.writer.add_scalar(data_nane + '/acc', acc, epoch)
            logging.info(
                '| epoch {:3d} | {} acc {:5d}/{:5d} = {:.2f} | time {:.2f}'.format(epoch, data_nane, corrects, totals,
                                                                                   acc,
                                                                                   during_time))

        return acc, pred_result, w_att_result, s_att_result

    def batch2tensor(self, batch_data):
        '''
            [[label, doc_len, [(sent_len, sent_id0, sent_id1), ...]], ...]
        '''
        batch_size = len(batch_data)
        doc_labels = []
        doc_lens = []
        doc_sent_lens = []
        doc_max_sent_len = []
        for doc_data in batch_data:
            doc_labels.append(doc_data[0])
            doc_lens.append(doc_data[1])
            sent_lens = [sent_data[0] for sent_data in doc_data[2]]
            doc_sent_lens.append(sent_lens)
            max_sent_len = max(sent_lens)
            doc_max_sent_len.append(max_sent_len)

        max_doc_len = max(doc_lens)
        max_sent_len = max(doc_max_sent_len)

        batch_inputs1 = torch.zeros((batch_size, max_doc_len, max_sent_len), dtype=torch.int64)
        batch_inputs2 = torch.zeros((batch_size, max_doc_len, max_sent_len), dtype=torch.int64)

        masks_dtype = torch.uint8 if self.config.word_encoder == "bert" else torch.float32
        batch_masks = torch.zeros((batch_size, max_doc_len, max_sent_len), dtype=masks_dtype)
        batch_labels = torch.LongTensor(doc_labels)

        for b in range(batch_size):
            for sent_idx in range(doc_lens[b]):
                sent_data = batch_data[b][2][sent_idx]
                for word_idx in range(sent_data[0]):
                    batch_inputs1[b, sent_idx, word_idx] = sent_data[1][word_idx]
                    batch_inputs2[b, sent_idx, word_idx] = sent_data[2][word_idx]
                    batch_masks[b, sent_idx, word_idx] = 1

        if self.config.use_cuda:
            batch_inputs1 = batch_inputs1.to(self.config.device)
            batch_inputs2 = batch_inputs2.to(self.config.device)
            batch_masks = batch_masks.to(self.config.device)
            batch_labels = batch_labels.to(self.config.device)

        return (batch_inputs1, batch_inputs2), batch_masks, batch_labels

    def logging_gpu_memory(self):
        """
        Get the current GPU memory usage.
        Based on https://discuss.pytorch.org/t/access-gpu-memory-usage-in-pytorch/3192/4
        Returns
        -------
        ``Dict[int, int]``
            Keys are device ids as integers.
            Values are memory usage as integers in MB.
            Returns an empty ``dict`` if GPUs are not available.
        """
        try:
            result = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=memory.used,memory.total",
                 "--format=csv,nounits,noheader"], encoding="utf-8",
            )
            info = [x.split(',') for x in result.strip().split("\n")]
            dic = {gpu: [int(mem[0]), int(mem[1])] for gpu, mem in enumerate(info)}
            gpu_id = self.config.gpu_id
            lst = dic[gpu_id]
            logging.info('| gpu id: {} | use {:5d}M / {:5d}M'.format(self.config.gpu_id, lst[0], lst[1]))

        except FileNotFoundError:
            # `nvidia-smi` doesn't exist, assume that means no GPU.
            return {}
        except:  # noqa
            # Catch *all* exceptions, because this memory check is a nice-to-have
            # and we'd never want a training run to fail because of it.
            logging.info("unable to check gpu_memory_mb(), continuing")
            return {}
