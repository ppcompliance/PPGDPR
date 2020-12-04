import pandas as pd
import re
import math
import os
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import word_tokenize, sent_tokenize

url_reg = r'(http|https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
url_reg2= r'[^\w+[^\s]+(\.[^\s]+){1,}$]'
email_reg = r"([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)"


def truncate_tokens_sent(tokens, max_sent):
    while True:
        words_len = [len(s) for s in tokens]
        if len(tokens) <= max_sent:
            break

        else:
            tokens.pop(words_len.index(min(words_len)))


def truncate_tokens_single(tokens, max_len):
    while True:
        if len(tokens) <= max_len:
            break
        else:
            tokens.pop()

def get_words(text):
    tokens = word_tokenize(text)

    return " ".join(tokens)


def get_word_count(text):
    text = text.replace('_', ' ')
    tokens = word_tokenize(text)
    words = [word for word in tokens if word.isalpha()]
    return len(words)


def write_line(mes, name):
    with open(name, "a", encoding="utf8") as f:
        if get_word_count(mes) > 0:
            f.write(mes+'\n')


def split_sent(s):
    s_list = re.split(r'[;。；]',s)
    return [i.strip() for i in s_list]


def filter_s(s):
    if len(s.strip()) > 0:
        if not s.strip()[0].isalnum() and not s.strip()[0].isalpha() and s.strip()[0] != '(' and s[:5] != '-url-' and s[:7] != '-email-' :
            return s.lstrip(s.strip()[0]).strip()
        else:
            return s.strip()


def check_label(mes):
    if mes in ['Policy_Introductory', 'First_Party_Collection_and_Use', 'Cookies_and_Similar_Technologies', 'Third_Party_Share_and_Collection',
               'User_Right_and_Control','Data_Security', 'Data_Retention', 'International_Data_Transfer', 'Specific_Audiences',
               'Policy_Change', 'Policy_Contact_Information']:
        return True
    else:
        return False


def get_data(file, file_open=True):
    res=[]
    # if file_open:
    #     with open(file, "r", encoding="utf8") as f:
    #         data = f.read().strip().split('\n')
    # else:
    data = file.strip().split('\n')
    for row in data:
        if get_word_count('Policy_Introductory') > 0:
            res.append('Policy_Introductory')
        a = sent_tokenize(row)
        for sentences in a:
            sent_token = word_tokenize(sentences)
            # truncate_tokens_single(sent_token, 128)

            if get_word_count(get_words(' '.join(sent_token))) > 0:
                res.append(get_words(' '.join(sent_token)))
        res.append('')
    return res


def get_lstm_data(data):
    return ["0\t"+str(i) for  i in data]

