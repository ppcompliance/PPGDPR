import BertPytorch.classify as classify
import re
import pandas as pd
import os


def get_bert_result(test_str):
    test_str = test_str.replace("e.g. ", "#E#G#")
    test_str = test_str.replace("Lnc. ", "#L#n#c#").replace("lnc. ", "#l#n#c#")
    test_str = test_str.replace("0. ", "#0#").replace("1. ", "#1#").replace("2. ", "#2#").replace("3. ", "#3#")
    test_str = test_str.replace("4. ", "#4#").replace("5. ", "#5#").replace("6. ", "#6#").replace("7. ", "#7#")
    test_str = test_str.replace("8. ", "#8#").replace("9. ", "#9#")
    test_str = test_str.replace("\n", ". #e#n#t#e#r#. ")
    test_list = test_str.split('. ')

    # 掐头
    pp_start_flag_num = 0
    pp_start_idx = 0
    for idx, line in enumerate(test_list):
        if pp_start_flag_num == 0 and len(line.split()) > 3:
            pp_start_idx = idx
            pp_start_flag_num += 1
        if pp_start_flag_num == 1 and line != "#e#n#t#e#r#":
            if len(line.split()) > 3: # 连续两个句子，单词数量同时都大于3，就算作开始privacy policy
                pp_start_flag_num = 2
                break
            else:
                pp_start_flag_num = 0
    print("start line:", pp_start_idx)

    # 去尾
    pp_end_flag_num = 0
    pp_end_idx = 0
    for idx in range(len(test_list) - 1, 0, -1):
        if pp_end_flag_num == 0 and len(test_list[idx].split()) > 3:
            pp_end_idx = idx
            pp_end_flag_num += 1
        if pp_end_flag_num == 1 and test_list[idx] != "#e#n#t#e#r#":
            if len(test_list[idx].split()) > 3: # 连续两个句子，单词数量同时都大于3，就算作结束privacy policy
                pp_end_flag_num = 2
                break
            else:
                pp_end_flag_num = 0
    print("end line:", pp_end_idx)

    # 写入文件
    file_test = open("BertPytorch/glue_data/file_test.tsv", 'w+', encoding='utf-8', errors='ignore')
    file_test.writelines("\tlabel\tsentence\n")

    for idx, line in enumerate(test_list):
        if idx >= pp_start_idx and idx <= pp_end_idx:
            if line != "":
                file_test.writelines(str(idx) + '\t' + '0' + '\t' + line + '\n')
    file_test.close()


    classify.main_classify()
    file_test_pd = pd.read_csv("BertPytorch/glue_data/file_test.tsv", delimiter='\t', sep='\t', encoding='utf-8')
    file_result_pd = pd.read_csv("BertPytorch/save/predict_result.tsv", delimiter='\t', sep='\t', encoding='utf-8')

    file_list = []
    para_list = []
    label_file_list = []
    label_para_list = []
    for idx, sentence in enumerate(file_test_pd.sentence):
        if sentence == "#e#n#t#e#r#":
            if para_list != []: # 去掉连续两个回车的情况
                file_list.append(para_list)
                label_file_list.append(label_para_list)
                para_list = []
                label_para_list = []
        else:
            if type(sentence) != str:
                sentence = " "
            sentence = sentence.replace("#E#G#", "e.g. ")
            sentence = sentence.replace("#L#n#c#", "Lnc. ")
            sentence = sentence.replace("#l#n#c#", "lnc. ")
            sentence = sentence.replace("#0#", "0. ").replace("#1#", "1. ").replace("#2#", "2. ").replace("#3#", "3. ")
            sentence = sentence.replace("#4#", "4. ").replace("#5#", "5. ").replace("#6#", "6. ").replace("#7#", "7. ")
            sentence = sentence.replace("#8#", "8. ").replace("#9#", "9. ")
            if idx < (len(file_test_pd.sentence) - 1) and file_test_pd.sentence[idx+1] != "#e#n#t#e#r#":
                para_list.append(sentence + ". ")
            else:
                para_list.append(sentence)
            label_para_list.append(file_result_pd.labelpredict[idx])

    label_compare = [0]*11
    detectissues = []
    for j in label_file_list:
        for i in j:
            label_compare[int(i)] = 1

    if label_compare[1] == 1:
        for i in range(2, 11):
            if label_compare[i] == 0:
                detectissues.append(i)

    data_para_list = []
    data_file_list = []
    for idx_i, i in enumerate(file_list):
        data_para_list = []
        for idx_j, j in enumerate(i):
            data_para_list.append({'label':str(label_file_list[idx_i][idx_j]),'text': j })
        data_file_list.append(data_para_list)
    return data_file_list, detectissues





if __name__ == '__main__':
    file_pp = open("BertPytorch/about.canva.com.txt", 'r', encoding='ANSI')
    str_privacy_policy = ""
    for line in file_pp:
        str_privacy_policy += line

    f_l, det = get_bert_result(str_privacy_policy)
    print(f_l)
    print(det)
