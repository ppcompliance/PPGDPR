import requests
from bs4 import BeautifulSoup,Comment
from src.util import *
from fake_useragent import UserAgent
from nltk.tokenize import word_tokenize, sent_tokenize
import re


class privacySpider:

    def get_word_count(self, text):
        tokens = word_tokenize(text)
        words = [word for word in tokens if word.isalpha()]
        return len(words)


    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        if re.match(r"[\s\r\n]+", str(element)):
            return False
        return True

    def clean(self, text):
        res = text.replace('\n', ' ')
        res = re.sub('\s+', ' ', res).strip()
        return res



    # def text_from_html(self, body):
    #     soup = BeautifulSoup(body, 'html.parser')
    #     texts = soup.findAll(text=True)
    #     visible_texts = filter(tag_visible, texts)
    #     return u" ".join(t.strip() for t in visible_texts)
    def data_clean(self, text):
        return text

    def parse_privacy(self, privacy_url):
        ua_headers = {'User-Agent': UserAgent().random}
        req = requests.get(url=privacy_url, headers=ua_headers)
        html = req.text
        soup = BeautifulSoup(html, "lxml")
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        visible_texts = [self.clean(t) for t in visible_texts]
        visible_texts = [t for t in visible_texts if self.get_word_count(t) > 0]
        return visible_texts

    def get_privacy(self, privacy_url, pp_id, app_id, name, **db_config):
        if pp_id < 0:
            try:
                text = self.parse_privacy(privacy_url)
                text = self.data_clean(str("\n".join(text)).strip())
                conn = pymysql.connect(host = db_config['host'], port = db_config['port'], user=db_config['user'],
                                       password = db_config['password'], db=db_config['database'])
                cursor = conn.cursor()
                query = 'insert into privacy_info(text, file_location, privacy_policy_link, app_id) ' \
                        'VALUES(%s,%s,%s,%s)'
                value = (text, name + ".html", privacy_url, int(app_id))
                try:
                    cursor.execute(query, value)
                    conn.commit()
                except:
                    conn.rollback()
                    return "Error: db error", False

                tag_id = cursor.lastrowid
                sql2 = "UPDATE gplay_info SET privacy_policy_id = '%d' WHERE app_id = '%d'" % (tag_id, app_id)
                try:
                    cursor.execute(sql2)
                    conn.commit()
                except:
                    conn.rollback()
                    return "Error: db error", False

                privacy_info = {'privacy_policy_id': pp_id, 'privacy_policy_link': privacy_url, 'app_id': app_id, 'text': text}
                return privacy_info, True
            except:

                return "Error: db error", False

        else:
            # try:
            engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(db_config['user'], db_config['password'],
                                                                           db_config['host'], db_config['port'],
                                                                           db_config['database']))
            sql = "Select * from privacy_info  WHERE privacy_policy_id = %d" % (pp_id)
            df_read = pd.read_sql_query(sql, engine)
            privacy_info = df_read.ix[0]

            return privacy_info, True
            # except:
            #     return "Error: db error", False

        # DBUtils.insertPrivacy(privacy_item_text,privacy_url)
        # print(privacy_item_text)
