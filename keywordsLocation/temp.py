import pymysql

keywords=[]
article_id=[]

def Get_data_in_sql():
    conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article')
    cur=conn.cursor()
    cur.execute('select distinct art_au_tags,article_id from acm_article where art_au_tags !=""')
    r=cur.fetchall()
    for r1 in r:
        keywords.append(r1[0])
        article_id.append(r1[1])

    conn.close()
    return keywords,article_id

keywords,article_id = Get_data_in_sql()


for i in range(len(keywords)):
        keywords[i] = keywords[i].split(";")


