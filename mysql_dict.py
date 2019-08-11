# mysql_dict.py
'''吧dict.txt中的内容按word,explains存入mysql数据库中'''
import pymysql
import re


def db_do():
    db = pymysql.connect(host='localhost',
                         port=3306, user='root',
                         password='123456', database='English_dict',
                         charset='utf8')
    cur = db.cursor()
    f = open('dict.txt')
    for data in f:
        if not data:
            break
        l = re.split(r'[ ]+',data)
        word = l[0]
        explains = ' '.join(l[1:])
        sql = 'insert into dict(word,explains) values(%s,%s);'
        try:
            cur.execute(sql, [word, explains])
            db.commit()
        except:
            db.rollback()
    cur.close()
    db.close()
    f.close()


if __name__ == '__main__':
    db_do()
