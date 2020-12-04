import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
class MySqlCon:
    def __init__(self, user='root', password='', host='localhost', port='3306', database='gplay'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(self.user, self.password,
                                                                       self.host, self.port,
                                                                       self.database), pool_size=20, max_overflow=0)

    def get_gdpr_info(self, detectiss):
        print("00000",detectiss)
        res = []
        for detect in detectiss:
            try:
                sql = "SELECT * FROM gdpr_consis WHERE gdpr_consis_id = '%d'" % (detect)
                df_read = pd.read_sql_query(sql, self.engine)
                detect_res = df_read.iloc[0].to_dict()
                detect_res['gdpr_consis_id'] = int(detect_res['gdpr_consis_id'] )
                print(detect_res)
                res.append(detect_res)
            except Exception:
                print(Exception)
                res.append(None)
        return res

    def get_app_info(self, gplay_id):
        '''
        获取数据库中app的信息
        :param glpy_id:
        :return:
        '''
        try:
            sql = "SELECT * FROM gplay_info WHERE gplay_id = '%s'" % (gplay_id)
            df_read = pd.read_sql_query(sql, self.engine)
            app_info_result = df_read.ix[0]
            return app_info_result
        except:
            return None
            # Exception("Error: unable to fetch data")
            # return "Error: select error", False


    def get_privacy_info(self,privacy_policy_link):
        try:
            sql = "SELECT * FROM privacy_info WHERE privacy_policy_link = '%s'" % (privacy_policy_link)
            df_read=pd.read_sql_query(sql, self.engine)
            return df_read.ix[0], True
        except:
            Exception("Error: unable to fetch data")
            return "Error: select error", False

    def insert_classification_from_pandas(self, data):
        con = self.engine.connect()
        try:
            data.to_sql(name='privacy_classification', con=con, if_exists='fail', index=False)
            return True
        except:
            return False

    def insert_info(self, item):
        '''
        插入新的app信息
        :param item:
        :return:
        '''
        print(item)

        con = self.engine.connect()
        error_mess = ""
        sql = "SELECT * FROM gplay_info WHERE gplay_id = '%s'" % (item['gplay_id'])
        df_read = pd.read_sql_query(sql, self.engine)
        if len(df_read) > 0:
            app_info = df_read.iloc[0]
            # print("000",app_info)
            error_mess = "Successful"
            return app_info, error_mess
        else:
            dict_data = {
                "app_name": [item['appname']],
                "app_link": [item['url']],
                "description": [item['description']],
                "privacy_policy_link": [item['privacy_url']],
                "update_time": [item['update']],
                "cur_version": [item['cur_version']],
                "app_size": [item['size']],
                "install_num": [item['download_num']],
                "version_require": [item['require']],
                "app_level": [item['level']],
                "offer": [item['dev_name']],
                "developer_web": [item['dev_web']],
                "developer_email": [item['dev_email']],
                "privacy_policy_id": [-1],
                "star": [item['star']],
                "category": [item['categories']],
                "gplay_id": [item['gplay_id']]
            }


            try:
                data = pd.DataFrame(dict_data)
                print("data", data)
                data.to_sql(name='gplay_info', con=con, if_exists='append', index=False)
                sql = "SELECT * FROM gplay_info WHERE gplay_id = '%s'" % (item['gplay_id'])
                df_read = pd.read_sql_query(sql, self.engine)
                if len(df_read) > 0:
                    app_info = df_read.ix[0]
                    error_mess = "Successful"
                    return app_info, error_mess
                else:
                    return None, "Error: select error"
            except:
                return None, "Error: insert error"

    def get_classification_data(self, category):
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(self.user, self.password,
                                                                       self.host, self.port,
                                                                       self.database))
        sql = "SELECT * FROM privacy_classification WHERE category = '%s'" % (category)
        df_read = pd.read_sql_query(sql, engine)
        return df_read

    #计算标签的比例：
def get_label_count(user='root', password='', host='http://211.81.52.44/', port='3306', database='gplay', category="all"):
    database = MySqlCon(user, password, host, port, database)
    result = database.get_classification_data(category)
    label_count = result.groupby('label').count()['data_id']
    print("lable_result", label_count)
    sum_val = label_count.sum()
    label_result = {'label_' + str(i): round((label_count[str(i)] / sum_val), 2) for i in range(len(label_count))}
    return label_result