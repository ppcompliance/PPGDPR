import pymysql
import config
import time
import mysql.connector
class DBUtils:
  def insertPrivacy(text,ppurl):
      print('-------------------------------------')
      try:
          mydb = mysql.connector.connect(host="localhost",
                                         user="root",
                                         passwd="",
                                         database="gplay")
          mycursor = mydb.cursor()
      except:
          print("connect mysql error")

      sql1 = "INSERT INTO privacy_info(privacy_policy_id,text,privacy_policy_link) VALUES(NULL,%s,%s)"
      val1 = (text, ppurl)
      try:
          mycursor.execute(sql1, val1)
          # 返回主键
          id = int(mycursor.lastrowid)
          print("privacy policy id",id)
          print(mycursor.rowcount, "privacy policy 记录插入成功。")
          mydb.commit()

      except:
          mydb.rollback()
          print("privacy policy 记录失败")
      mydb.close()



  def dbInsert(item):
      try:

          mydb = mysql.connector.connect(host="localhost",
                                         user="root",
                                         passwd="",
                                         database="gplay")
          mycursor = mydb.cursor()
      except:
          print("connect mysql error")
      sql1 = "INSERT INTO gplay_info(app_name,app_link,description,privacy_policy_link,update_time,cur_version,app_Size,install_num,version_require,app_level,offer,developer_web,developer_email,privacy_policy_id,star,category,gplay_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,%s,%s,%s)"
      val1 = (
          item['appname'], item['url'], item['description'], item['privacy_policy'], item['update'],
          item['cur_version'],
          item['size'], item['download_num'], item['require'], item['level'], item['dev_name'], item['dev_web'],
          item['dev_email'],
          item['star'], item['categories'],item['app_id'])
      try:
          mycursor.execute(sql1,val1)
          # 返回主键
          id = int(mycursor.lastrowid)
          print("app id",id)
          print(mycursor.rowcount, "记录插入成功。")
          mydb.commit()
      except:
          mydb.rollback()
          print("0000失败")
      mydb.close()


  def SelectApp(name):
      try:

          mydb = mysql.connector.connect(host="localhost",
                                         user="root",
                                         passwd="",
                                         database="gplay")
          mycursor = mydb.cursor()
      except:
          print("connect mysql error")

      sql2= 'SELECT * FROM gplay_info WHERE app_link="'+name+'"'


      try:
          mycursor.execute(sql2)
          mydb.commit()
      except:
          mydb.rollback()
          print("0000失败")
      mydb.close()



