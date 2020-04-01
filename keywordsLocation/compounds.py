import csv
import pymysql
import matplotlib.pyplot as plt
import nltk.data
from nltk.tokenize import WordPunctTokenizer


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

# print(len(keywords))
# print(len(article_id))

for i in range(len(keywords)):
        keywords[i] = keywords[i].split(";")

contain_compounds = []
count = 0
for i in range(len(keywords)):
    for j in range(len(keywords[i])):
        if ' ' in keywords[i][j]:
            count = count + 1

    contain_compounds.append(count/len(keywords[i]))
    count = 0

header = ['article_id','keywords','contain_compounds']
with open(r"C:\Users\hjn\Desktop\关键词课题\compounds_keyword.csv","w",encoding= 'utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(article_id, keywords,contain_compounds))
csvfile.close()

p=[0,0,0,0,0,0]

for i in contain_compounds:
    if i == 0:
        p[0] = p[0]+1

    elif i - 0.25 <=0:
        p[1] = p[1]+1
    elif i - 0.5 <=0:
        p[2] = p[2]+1
    elif i - 0.75 <=0:
        p[3] = p[3]+1
    elif i - 1 <0:
        p[4] = p[4]+1
    else:
        p[5] = p[5]+1

print(p)


