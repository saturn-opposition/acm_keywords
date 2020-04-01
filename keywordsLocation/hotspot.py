import csv
import pymysql
import nltk.data
from nltk.tokenize import WordPunctTokenizer
import re

keywords=[]
article_id=[]
year = []
title = []
abstract = []
def Get_data_in_sql():
    conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article')
    cur=conn.cursor()
    cur.execute('select  art_au_tags,article_id,art_pub_year,art_title,art_abstract from acm_article where art_au_tags !=""')
    r=cur.fetchall()
    for r1 in r:
        if r1[0] not in keywords:
            keywords.append(r1[0])
            article_id.append(r1[1])
            year.append(r1[2])
            title.append(r1[3])
            abstract.append(r1[4])
    conn.close()
    return keywords,article_id,year,title,abstract

keywords,article_id,year,title,abstract = Get_data_in_sql()

words = []
for i in range(len(keywords)):
        keywords[i] = keywords[i].split(";")
        for j in range(len(keywords[i])):
            words.append(keywords[i][j])


for s in title:
    temp = WordPunctTokenizer().tokenize(s)
    for w in temp:
        words.append(w)

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for i in range(len(abstract)):
    sentences = tokenizer.tokenize(abstract[i])
    for s in sentences:
        temp = WordPunctTokenizer().tokenize(s)
        for w in temp:
            words.append(w)

words_dict = {}
count = 0
stop_words_file = open(r"C:\Users\hjn\Desktop\关键词课题\英文停用词.txt",encoding='utf-8',errors = 'ignore').read()  #去掉英文停用词
stop_words = re.split('\n',stop_words_file)
for i in range(len(words)):
    if (words[i] not in stop_words) & (words[i] not in words_dict.keys()):
        words_dict[words[i]] = 1
    if (words[i] not in stop_words) & (words[i] in words_dict.keys()):
        count = words_dict[words[i]]
        words_dict[words[i]] = count + 1



for key,value in words_dict.items():
    print(key+':'+str(value))

header = ['words','frequency']
with open(r"C:\Users\hjn\Desktop\关键词课题\word_frequency.csv","w",encoding= 'utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(words_dict.keys(),words_dict.values()))
csvfile.close()



