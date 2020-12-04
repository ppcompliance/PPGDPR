
import re
import string
import json
import math
import pandas as pd
import nltk
from preprocess import merge
from nltk.tokenize import word_tokenize
urlReg = r"^(?:([A-Za-z]+):)?(\/{0,3})([0-9.\-A-Za-z]+)(?::(\d+))?(?:\/([^?#]*))?(?:\?([^#]*))?(?:#(.*))?$"
entityRe = r'\[\@.*?\#.*?\*\](?!\#)'


def check_tag(s):
    nltk.corpus.brown.tagged_words ()
    related_tag = ['VB', 'VBP', 'VBZ', 'VBD', 'VBN']
    s = nltk.word_tokenize (s)
    s_pos = nltk.pos_tag (s)
    for w_pair in s_pos:
        if w_pair[1] in related_tag:
            return True
    return False


def get_word_count(text, returnsequences=False, retuenlist = False):
    tokens = word_tokenize(text)
    words = [word for word in tokens if re.search(r"[\w]", word)]
    if returnsequences:
        return " ".join(words)
    elif retuenlist:
        return words
    else:
        return len(words)


def check_have_ul_merge(text):
    if re.search(r"\[@start#\]", text.lower()) is None:
        return False
    else:
        return True


def unrelated(text):
    punc = r"""!"'()*,-.:;?~"""
    word_list = get_word_count(text, retuenlist=True)
    if len(word_list) == 0:
        return True
    return len(word_list) <= 8 and text.strip()[-1] not in punc


def check_unrelated(text):
    punc = r"""!"'()*,-.:;?~"""
    num = 0
    text_list = [i for i in text if get_word_count(i) > 0 and
                 re.search(r"©", i) is None and
                 re.search(r"powered by", i.lower()) is None]
    if len(text_list) == 0:
        return True
    for i in text_list:
        word_list = get_word_count(i, retuenlist=True)
        word_list = [i.strip() for i in word_list if len(i.strip()) > 0]
        if len(word_list) <= 0:
            continue
        if (len(word_list) <= 10 and i.strip()[-1] not in punc) or not check_tag(i):
            num += 1
    if len(text_list) - num == 0:
        return True
    if len(text_list) - num > 2:
        return False

    if num > len(text_list) - num + 2:
        return True
    else:
        return False


def print_unrelated(lst):
    for i in lst:
        if check_have_ul_merge(i):
            [print(j) for j in i.split("[@Start#]")]
        else:
            print(i)


def remove_unrelated(para):
    result = [i for i in para]
    for i in para:
        if not check_unrelated(i):
            break
        else:
            print_unrelated(i)
            result.remove(i)

    for i in reversed(para):
        if not check_unrelated(i):
            break
        else:
            print_unrelated (i)
            result.remove(i)

    return result


def clean_list(lst):
    return [i for i in lst if len(i.strip()) > 0]


def get_lst_rate(data):
    words = [get_word_count(i) for i in data]
    max_length = max(words)
    all_length = sum(words)
    index = words.index(max_length)
    return (index,True) if max_length/all_length > 0.7 else (index,False)


def predict_preprocess(document):

    # document = [i for i in document.split('\n') if len(i.strip()) > 0]
    # result = []
    #
    # for i in document:
    #     if check_have_ul_merge(i):
    #         result.append([j for j in i.split("[@Start#]") if len(i.strip()) > 0])
    #     else:
    #         result.append([i])

    # result = remove_unrelated(result)

    document = merge.MergeFollows(document).merge
    # print('\n'.join(document))

    result = []
    for par_lst in document:
        if len(par_lst) == 1 and len(par_lst[0].strip()) > 0:
            if check_have_ul_merge(par_lst[0]):
                par_lst[0] = par_lst[0].lower()
                result.append(clean_list(par_lst[0].split('[@start#]')))
            else:
                result.append([par_lst[0].strip()])
        elif len(par_lst) > 1:
            result.append([])
            for par in par_lst:
                if len(par.strip()) > 0:
                    if check_have_ul_merge(par):
                        par = par.lower()
                        [result[-1].append(i) for i in clean_list(par.split('[@start#]'))]
                    else:
                        result[-1].append(par.strip())
    result = remove_unrelated(result)
    result = [i for i in result if not text_unrelated(i)]
    test_data = []
    for i in result:
        if len(i) == 1:
            test_data.append(i[0])
        elif len(i) > 1:
            #
            test_data.append(";".join(i))
        else:
            pass

    max_index, is_flatten = get_lst_rate(test_data)
    if is_flatten:
        new_data_origin = [result[i] for i in range(0, max_index)]
        for i in result[max_index]:
            new_data_origin.append ([i])
        for i in range (max_index + 1, len (result)):
            new_data_origin.append (result[i])
        result = new_data_origin

        test_data = []
        for i in result:
            if len (i) == 1:
                test_data.append (i[0])
            elif len (i) > 1:
                #
                test_data.append (";".join (i))
            else:
                pass
    return result, test_data


def text_unrelated(texts):
    num = 0
    for text in texts:
        if re.search(r"©", text) is not None:
            return True
        if get_word_count(text) <= 1:
            num += 1
    if num == len(texts):
        return True

