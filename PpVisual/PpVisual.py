# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, jsonify
from flask_cors import *
from nltk.tokenize import word_tokenize, sent_tokenize
from Spider.crawel_gplay_info import scrape_info
from src.classification import *
from src.label_pre import *
from out_attention import get_han_result
from lstm_train import get_lstm_result
import base64
import json
import csv
import os
import time
import yake
import pandas as pd
from nltk.corpus import stopwords
import nltk
import re
import math
from collections import Counter

from urllib.parse import unquote
# import crochet
#
# crochet.setup()
# import sys
# sys.path.extend(["../../", "../", "./"])
DIR = os.path.dirname(__file__)
from DBconf.dbutil import MySqlCon, get_label_count
from DBconf.privacySpider import privacySpider
import pymysql
from werkzeug.utils import secure_filename, redirect

label_list = ["Introductory", "How We Collect and Use Your Information", "Cookies and Similar Technologies",
              "Third Party Sharing and Collection", "What You Can Do", "How We Protect Your Information",
              "Data Retention", "International Data Transfer", "Specific Audiences", "Policy Change",
              "Contact Information"]

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def hello_world():
    return render_template('content/content.html')
    # return 'Hello World!'
# @app.route('/submit',methods=['POST','GET'])
# def submit():
#     text_result={}
#     url_data = request.get_data()
#     json_re = json.loads(url_data)
#     url= json_re['url']
#     name,info,category_info,label_setnum=content(url)
#     text_result['name'] = name
#     text_result['info'] = info
#     text_result['category_info'] = category_info
#     text_result['label_setnum'] =label_setnum
#     print(text_result)
#
#     return json.dumps(text_result)


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    '''
    提交app url 信息传入爬虫
    :return:
    '''
    if request.method == 'POST':
        url = request.form['AppUrl']
        button_name = request.form['submitbutton']
        # url_encode = url.encode()
        # print(url_encode)
        # miss_padding = 4 - len(url_encode) % 4
        # if miss_padding:
        #     url_encode += b'=' * miss_padding
        # urls = base64.b64decode(url_encode)
        # print(urls)
        if button_name == "隐私政策内容分析":
            return redirect(url_for('content', url=url))
        elif button_name == "合规性分析":
            return redirect(url_for('Compliance', url=url))
    else:
        return redirect(url_for('error/error.html'))
@app.route("/content",methods=['POST', 'GET'])
def content():
    '''
    查找数据库中是否包含该app的隐私政策
    如果没有则进行爬虫抓取。如果存在则直接读取出来。
    :return:
    '''
    text_result = {}
    dict_num = {}
    result = []
    key = []
    csv_result = []
    global info
    global category_info
    db_config = {'user': 'root', 'password': '', 'host': 'localhost', 'port': 3306, 'database': 'gplay'}
    con = MySqlCon(user=db_config['user'], password=db_config['password'], host=db_config['host'],
                   port=db_config['port'], database=db_config['database'])
    baseURL = request.args.get('url')
    print("1111",baseURL)
    # baseURL = base64.b64decode(url).decode("utf-8")
    print("111",baseURL)
    if not baseURL.strip().endswith('&hl=zh'):
        baseURL = baseURL.strip() + '&hl=zh'
    gplay_id = baseURL.split('&')[-2].split('=')[-1]
    #查询数据库是否存在该app信息,如果为None则进行爬虫抓取app information
    #如果存在则直接获取privacy policy url进行隐私文本抓取
    app_res = con.get_app_info(gplay_id)
    # print("sel_red",sel_res)
    if app_res is None:
        app_item = scrape_info(baseURL)
        # print(app_item)
        app_res, error_mess = con.insert_info(app_item)
        # print(error_mess)

    # if not sel_res:
    #     app_item = scrape_info(baseURL)
    #     #插入数据
    #     app_res, error_mess = con.insert_info(app_item)

    if app_res is not None:
        privacy_info,error_mess = privacySpider().get_privacy(privacy_url=app_res['privacy_policy_link'],
                                                           pp_id=app_res['privacy_policy_id'], app_id=app_res['app_id'],
                                                           name=app_res['gplay_id'], **db_config)
        print(privacy_info)



        label_num = []
        p, data, w_att_result = get_han_result(privacy_info['text'])

        con = MySqlCon(user='root', password='', host='localhost', port='3306', database='gplay')
        info = {"app_name": app_res['app_name'], "category": app_res["category"], "star": app_res["star"],
                "install_num": app_res['install_num'], "offer": app_res['offer'],
                "update_time": app_res['update_time'], "pp_link": app_res['privacy_policy_link'],
                "description": app_res['description']}
        category_info = get_label_count(user='root', password='', host='localhost', port='3306', database='gplay',
                                        category='all')
        classification_insert_data = []
        for i, value in enumerate(p):
            result_dict = {'review': data[i].strip(), "label": str(value), "word_weight": str(w_att_result[i])}
            classification_insert_data.append(
                [app_res['privacy_policy_id'], data[i], '|||'.join(sent_tokenize(data[i])), value, app_res['app_id'],
                 str(time.time())])
            con.insert_classification_from_pandas(
                pd.DataFrame(classification_insert_data, columns=['privacy_policy_id', 'par', 'sentences', 'label',
                                                                  'category', 'insert_time']))
            result.append(result_dict)
            label_num.append(str(value))
        label_set = set(label_num)
        print(label_set)
        # dict_num = {}
        for item in label_num:
            dict_num.update({'label_' + item: round(label_num.count(item) / len(label_num), 2)})

        label00(dict_num)
        label01(dict_num)
        label02(dict_num)
        label03(dict_num)
        label04(dict_num)
        label05(dict_num)
        label06(dict_num)
        label07(dict_num)
        label08(dict_num)
        label09(dict_num)
        label10(dict_num)
        print((dict_num))
        # name = json.dumps(result)

        category_info = category_info
        # label_setnum = dict_num
        '''
        name:标签+文本+权重值
        info：APP信息
        category_info:同类型APP标签的分布（柱状图）
        label_setnum：APP标签的分布
        '''
        '''
        提取关键字：
        '''
        pp_text = privacy_info['text']
        kw_extractor = yake.KeywordExtractor(lan='en', n=3, dedupLim=0.9, dedupFunc='seqm', windowsSize=2, top=80,
                                             features=None)
        keyword = kw_extractor.extract_keywords(pp_text)

        for kw in keyword:
            key.append(kw)
        name_result = list(set(key))
        columens = ['word', 'weight']
        entity_fram = pd.DataFrame(name_result, columns=columens)
        key = entity_fram.to_dict('records')
        '''
        获取同类型隐私政策的所有标签
        '''


        csv_file=open(DIR+'\\static\\data\\tsne.csv', 'r')

        reader = csv.DictReader(csv_file)

        for row in reader:
            csv_text = {}
            for k,v in row.items():
                csv_text[k] = v
            csv_result.append(csv_text)
        print(csv_result)

    return render_template('content/contentindex.html',name=json.dumps(result), info=info, category_info=category_info,
                               label_setnum=dict_num,key_result=key,csv_text=json.dumps(csv_result))
#
#


def keyword(word):
    word = word
    stop_words = stopwords.words('english')
    tokens = [token for token in word if token not in stop_words]
    return tokens

def word2vec(word):
    cw = Counter(word)
    sw = set(cw)
    lw = math.sqrt(sum(c * c for c in cw.values()))
    return cw, sw, lw
def removePunctuations(str_input):
    ret = []
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for char in str_input:
        if char not in punctuations:
            ret.append(char)

    return "".join(ret)
def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]

@app.route("/Compliance")
def Compliance():
    conn = pymysql.connect(host='localhost', user='root', password='', db='gplay', charset='utf8')
    cur = conn.cursor()
    cur1 = conn.cursor()
    sql = "SELECT label FROM pp_com"
    sql1 = "SELECT label_sum FROM pp_com"
    cur.execute(sql)
    cur1.execute(sql1)
    label = cur.fetchall()
    label_sum = cur1.fetchall()
    conn.close()
    '''
    合规性检测
    :return:
    '''

    db_config = {'user': 'root', 'password': '', 'host': 'localhost', 'port': 3306, 'database': 'gplay'}
    con = MySqlCon(user=db_config['user'], password=db_config['password'], host=db_config['host'],
                   port=db_config['port'], database=db_config['database'])
    baseURL = request.args.get('url')
    print("1111", baseURL)
    # baseURL = base64.b64decode(url).decode("utf-8")
    if not baseURL.strip().endswith('&hl=zh'):
        baseURL = baseURL.strip() + '&hl=zh'
    gplay_id = baseURL.split('&')[-2].split('=')[-1]
    app_res = con.get_app_info(gplay_id)
    # print("sel_red",sel_res)
    if app_res is None:
        app_item = scrape_info(baseURL)
        # print(app_item)
        app_res, error_mess = con.insert_info(app_item)
        # print(error_mess)

    # if not sel_res:
    #     app_item = scrape_info(baseURL)
    #     #插入数据
    #     app_res, error_mess = con.insert_info(app_item)
    if app_res is not None:
        privacy_info, error_mess= privacySpider().get_privacy(privacy_url=app_res['privacy_policy_link'],
                                                   pp_id=app_res['privacy_policy_id'], app_id=app_res['app_id'],
                                                   name=app_res['gplay_id'], **db_config)

        # print(privacy_info['text'])


        result = []
        label_num = []
        p, data, w_att_result, detectiss = get_lstm_result(privacy_info['text'])
        # print("PPP", p)
        # print("##V#V#", detectiss)
        '''
        如果detectiss返回为null的话说明隐私政策没有违规
        '''
        con = MySqlCon(user='root', password='', host='localhost', port='3306', database='gplay')
        print("detectiss",detectiss)
        gdpr_info = con.get_gdpr_info(detectiss)
        print("gdpr_info", gdpr_info)
        info = {"app_name": app_res['app_name'], "star": app_res["star"],
                "install_num": app_res['install_num'], "offer": app_res['offer'],
                "update_time": app_res['update_time'], "pp_link": app_res['privacy_policy_link'],
                "description": app_res['description']}
        category_info = get_label_count(user='root', password='', host='localhost', port='3306', database='gplay',
                                        category='all')
        classification_insert_data = []
        for i, value in enumerate(p):
            try:
                data_review = data[i].strip()
            except:
                continue
            result_dict = {"review": data_review, "label": str(value), "weight": str(w_att_result[i])}
            classification_insert_data.append(
                [app_res['privacy_policy_id'], data[i], '|||'.join(sent_tokenize(data[i])), value, app_res['app_id'],
                 str(time.time())])
            result.append(result_dict)
            label_num.append(str(value))

        label_set = set(label_num)
        # print(label_set)
        dict_num = {}
        for item in label_num:
            dict_num.update({'label_' + item: round(label_num.count(item) / len(label_num), 2)})

        label00(dict_num)
        label01(dict_num)
        label02(dict_num)
        label03(dict_num)
        label04(dict_num)
        label05(dict_num)
        label06(dict_num)
        label07(dict_num)
        label08(dict_num)
        label09(dict_num)
        label10(dict_num)
        # print((dict_num))
        # print(result)
        # print("gdpr", gdpr_info)

        '''
        提取关键字
        '''
        sent_result=[]
        f = privacy_info['text']
        remove_chars = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        word_token = re.sub(remove_chars,'',f)
        sent = nltk.word_tokenize(word_token.lower())
        for sent in sent:
            sent_result.append(sent)
        token = keyword(sent_result)
        key_result = []
        for i in token:
            token_words = (
            removePunctuations(i), cosdis(word2vec(removePunctuations(i)), word2vec(removePunctuations("compliance"))))
            key_result.append(token_words)
        name_result = list(set(key_result))
        columens = ['word', 'weight']
        entity_fram = pd.DataFrame(name_result, columns=columens)
        keyGdprWord = entity_fram.to_dict('records')
        # print(keyGdprWord)



        return render_template('Compliance/Compliance.html', gdpr_data=result, info=info, category_info=category_info,
                               label_setnum=dict_num, u=label, sum=label_sum, gdpr=gdpr_info,keyGdprWord=json.dumps(keyGdprWord))
@app.route("/base", methods=['POST', 'GET'])
def base():

    pass
@app.route('/pp_index', methods=['POST', 'GET'])
def pp_index():
    if request.method == 'POST':
        # url1 = request.referrer,
        url2= request.form['AppUrl']
        if url2 =="" :
            url1 = request.referrer
            surl = url1.split('url=')[1]
            baseURL = unquote(surl, 'utf-8')
            button_name = request.form['submitbutton']
            if button_name == "隐私政策内容分析":
                return redirect(url_for('content', url=baseURL))
            elif button_name == "合规性分析":
                return redirect(url_for('Compliance', url=baseURL))

            print(url2)
            print("0000")
        else:
            print("----",url2)
        # for url in url2,url1:
        #     if url is url1:
        #         surl = url.split('url=')[1]
        #         baseURL = unquote(surl, 'utf-8')
        #         if button_name == "隐私政策内容分析":
        #             return redirect(url_for('content', url=baseURL))
        #         elif button_name == "合规性分析":
        #             return redirect(url_for('Compliance', url=baseURL))
        #     if url is url2:
        #         print("-----url------", url)
        #         button_name = request.form['submitbutton']
        #         if button_name == "隐私政策内容分析":
        #             return redirect(url_for('content', url=url))
        #         elif button_name == "合规性分析":
        #             return redirect(url_for('Compliance', url=url))
        # for url in request.form['AppUrl'], request.referrer:
        #     if url is not request.referrer:









# from gevent.pywsgi import WSGIServer
# from gevent import monkey
#
# # WSGIServer(("127.0.2.76",5000),app).serve_forever()
import schedule
import time
if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    # monkey.patch_all()
    # app.run(host='0.0.0.0', port=8090, debug=True)
    # WSGIServer(("127.0.2.76",5000),app).serve_forever()
    # 127.0.0.100
    schedule.every(10).seconds.do(app.run(host='0.0.0.0', port=5000, debug=True))

