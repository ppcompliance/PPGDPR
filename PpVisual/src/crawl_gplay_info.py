import requests
import time
from fake_useragent import UserAgent
from lxml import etree


def scrape_info(url, chinese=True):

    ua_headers = {'User-Agent': UserAgent().random}
    if (not url.strip().endswith('&hl=zh')) and chinese:
        url = url.strip() + '&hl=zh'

    html = requests.get(url, headers=ua_headers)
    html.encoding = 'utf8'
    r = html.content
    selector = etree.HTML(r, parser=etree.HTMLParser(encoding='utf8'))
    time.sleep(5)

    item = dict()

    privacy_policy = selector.xpath('//div[contains(text(),"开发者")]/..//a[contains(text(),"隐私权政策")]/@href')
    if len(privacy_policy) > 0:
        privacy_policy = privacy_policy[0]
    item['url'] = url

    gplay_id = url.split('&')[-2].split('=')[-1]

    if gplay_id:
        item['gplay_id'] = gplay_id
    else:
        item['gplay_id'] = ''
    appname = selector.xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/c-wiz[1]/h1/span/text()')
    if (len(appname) > 0):
        appname = appname[0]
    a = type(appname)
    print(a)
    # 类别
    categories = selector.xpath(
        '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[1]/div/div[1]/div[1]/span[2]/a/text()')
    if len(categories) > 0:
        categories = categories[0]
    # 描述
    description = selector.xpath('//*[@id="fcxH9b"]//meta[@itemprop="description"]/@content')

    description = description[0] if len(description) else ""


    description = description.replace("\n", "<br>")


    rating = dict()
    rating['overall'] = selector.xpath('//*[@id="fcxH9b"]//div[@class="BHMmbe"]/text()')
    if (len(rating['overall']) > 0):
        rating['overall'] = rating['overall'][0]
    else:
        rating['overall'] = "0"
    ratings = selector.xpath('//span[@title]//@title')
    if (len(ratings) > 0):
        rating['five_star'] = ratings[0]
    else:
        rating['five_star'] = "0"
    if (len(ratings) > 1):
        rating['four_star'] = ratings[1]
    else:
        rating['four_star'] = "0"
    if (len(ratings) > 2):
        rating['three_star'] = ratings[2]
    else:
        rating['three_star'] = "0"
    if (len(ratings) > 3):
        rating['two_star'] = ratings[3]
    else:
        rating['two_star'] = "0"
    if (len(ratings) > 4):
        rating['one_star'] = ratings[4]
    else:
        rating['one_star'] = "0"
    rating["total_rating"] = selector.xpath('//span[@aria-label]/text()')

    if (len(rating['total_rating']) > 0):
        rating['total_rating'] = rating['total_rating'][0]
    else:
        rating['total_rating'] = "0"

    # 更新日期
    item['update'] = selector.xpath('//div[contains(text(),"更新日期")]/..//span/text()')
    if (len(item['update']) > 0):
        item['update'] = item['update'][0]
    else:
        item['update'] = ""
    # 大小
    item['size'] = selector.xpath('//div[contains(text(),"大小")]/..//span/text()')
    if (len(item['size']) > 0):
        item['size'] = item['size'][0]
    else:
        item['size'] = ""
    # 下载人数
    item['download_num'] = selector.xpath('//div[contains(text(),"安装次数")]/..//span/text()')
    if (len(item['download_num']) > 0):
        item['download_num'] = item['download_num'][0]
    else:
        item['download_num'] = ""
    # 版本
    item['cur_version'] = selector.xpath('//div[contains(text(),"当前版本")]/..//span/text()')
    if (len(item['cur_version']) > 0):
        item['cur_version'] = item['cur_version'][0]
    else:
        item['cur_version'] = ""
    # 要求
    item['require'] = selector.xpath('//div[contains(text(),"Android 系统版本要求")]/..//span/text()')
    if (len(item['require']) > 0):
        item['require'] = item['require'][0]
    else:
        item['require'] = ""
    # 内容分级
    item['level'] = selector.xpath('//div[contains(text(),"内容分级")]/../span//div/text()')
    if (len(item['level']) > 0):
        item['level'] = '`'.join(item['level'])
    else:
        item['level'] = ""

    # 开发网站
    item['dev_web'] = selector.xpath('//div[contains(text(),"开发者")]/..//a/@href')
    if (len(item['dev_web']) > 0):
        item['dev_web'] = item['dev_web'][0]
    else:
        item['dev_web'] = ""
    # 开发人员Email
    item['dev_email'] = selector.xpath('//div[contains(text(),"开发者")]/..//a/@href')
    if (len(item['dev_email']) > 2):
        item['dev_email'] = item['dev_email'][1]
    else:
        item['dev_email'] = ""
    # 开发人员名字
    item['dev_name'] = selector.xpath('//div[contains(text(),"开发者")]/..//div/text()')
    if (len(item['dev_name']) > 0):
        item['dev_name'][0] = ""
        item['dev_name'] = ''.join(item['dev_name'])
    else:
        item['dev_name'] = ""

    item['privacy_url'] = privacy_policy
    item['appname'] = appname
    item['categories'] = categories
    item['description'] = description
    item["rating"] = "one_star:" + rating["one_star"] + ";" + "two_star:" + rating[
        "two_star"] + ";" + "three_star:" + rating["three_star"] + ";" + "four_star:" + rating[
                         "four_star"] + ";" + "five_star:" + rating["five_star"] + ";" + "total_rating:" + rating[
                         "total_rating"] + ";" + "overall:" + rating["overall"]

    item['star'] = rating["overall"]
    return item
