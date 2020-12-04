"""
 　　#!/usr/bin/python3
    Author: RjMonkey  
    Date: 2019/12/12
"""
import os
#

task = 'pp'

# os.system('python classify.py \
#             --task '+task+' \
#             --mode train \
#             --train_cfg config/train_mrpc.json \
#             --model_cfg config/bert_base.json \
#             --data_file glue_data/'+task+'/train.tsv \
#             --pretrain_file model/bert_model.ckpt \
#             --vocab model/vocab.txt \
#             --save_dir save/ \
#             --max_len 128')

os.system('python classify.py \
    --task '+task+' \
    --mode eval \
    --train_cfg config/train_mrpc.json \
    --model_cfg config/bert_base.json \
    --data_file glue_data/'+task+'/test.tsv \
    --model_file save/model_steps_346.pt \
    --vocab model/vocab.txt \
    --max_len 128')
