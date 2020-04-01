import pymysql
import nltk
import csv
import re
import nltk.data
from nltk.tokenize import WordPunctTokenizer
id = []
abstract = []
keywords = []

with open("F:\\acm_data\keywords_in_abstract.csv",'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        id.append(row[0])
        keywords.append(row[1])

keywords.remove('keywords')
id.pop(0)

conn=pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab',db='acm_acm_article',use_unicode = True,charset = 'utf8')
cur=conn.cursor()

for i in range(len(id)):
    cur.execute('select  art_abstract from acm_article where article_id = "'+id[i]+'"')
    r=cur.fetchall()
    for r1 in r:
        abstract.append(r1[0])

for i in range(5):
    print(keywords[i]+"***"+abstract[i])

for i in range(len(keywords)):
    keywords[i] = re.findall(r'\[(.+?)\]',keywords[i])
    keywords[i] = keywords[i][0].split(',')
    for j in range(len(keywords[i])):
        keywords[i][j] = keywords[i][j].replace('\'','')



tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')



for i in range(50):
    wordslist = []
    sentences = tokenizer.tokenize(abstract[i])
    for s in sentences:
        words = WordPunctTokenizer().tokenize(s)
        wordslist.extend(words)
    print(wordslist)
    text = nltk.text.Text(wordslist)
    text.dispersion_plot(keywords[i])

