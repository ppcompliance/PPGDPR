"""
 　　#!/usr/bin/python3
    Author: RjMonkey  
    Date: 2019/11/2

    预处理文本
"""

import re
import nltk
from collections import Iterable
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


def flatten(lst):
    for item in lst:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


def clean_text(sentence):
    # 过滤不了\\ \ 中文（）还有————
    r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'  # 用户也可以在此进行自定义过滤字符
    # 者中规则也过滤不完全
    r2 = "[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"
    # \\\可以过滤掉反向单杠和双杠，/可以过滤掉正向单杠和双杠，第一个中括号里放的是英文符号，第二个中括号里放的是中文符号，第二个中括号前不能少|，否则过滤不完全
    r3 = "[.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）]+"
    # 去掉括号和括号内的所有内容
    r4 = "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"
    cleanr = re.compile('<.*?>')
    sentence = re.sub(cleanr, ' ', sentence)  # 去除html标签
    sentence = re.sub(r4, '', sentence)
    return sentence


def remove_stopwords(words):
    filter_sentence = [w for w in words if w not in stopwords.words('english')]
    return filter_sentence


def word_stemming(words):
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(i) for i in words]


def word_lemmatization(words):
    wnl = WordNetLemmatizer()
    return [wnl.lemmatize(i) for i in words]


def text_preprocess(text, is_lower=True, method=None):
        if method is None:
            return clean_text(text).lower() if is_lower else clean_text(text)
        words = nltk.word_tokenize(text=text)
        for i in flatten([method]):
            assert i in ["stopwords", "stemming", "lemmatization"]
            if i == 'stopwords':
                words = remove_stopwords(words)
            if i == 'stemming':
                words = word_stemming(words)
            if i == 'lemmatization':
                words = word_lemmatization(words)

        return clean_text(" ".join(words)).lower()




