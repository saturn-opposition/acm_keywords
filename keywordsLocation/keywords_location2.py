import pymysql
import nltk
import csv
import re
import nltk.data
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import  WordNetLemmatizer
import  matplotlib.pyplot as plt

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab', db='acm_keyword', use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
cursor.execute("select article_id,art_abstract,art_au_tags from acm_article_final ")
row = cursor.fetch(100)
article_id = []
art_abstract = []
art_au_tags = []
for i in range(len(row)):
   article_id.append(row[i][0])
   art_abstract.append(row[i][1])
   art_au_tags.append(row[i][2])

lemmatizer=WordNetLemmatizer()
all_dict = []
art_all_tags = []
for i in range(len(art_au_tags)):
    all_occur_tags = []
    words = []
    tags = []
    this_art_dict = {}
    tags_temp = art_au_tags[i].lower().split(';')
    abstract = art_abstract[i]
    words_temp = WordPunctTokenizer().tokenize(abstract)
    for t in range(len(words_temp)):
        l = lemmatizer.lemmatize(words_temp[t])
        words.append(l.lower())

    for t in range(len(tags_temp)):

        for j in range(len(words)):
            if words[j]==tags_temp[t]:
                if words[j] in this_art_dict.keys():
                    str = this_art_dict[words[j]] +";"+str(j/len(words))
                    this_art_dict[words[j]] = str
                    all_occur_tags.append(tags_temp[t])
                else:
                    this_art_dict[words[j]] = str(j/len(words))
    all_dict.append(this_art_dict)
    art_all_tags.append(';'.join(all_occur_tags))
header = ['article_id','tags','occur','location']
with open("C:\\Users\\hjn\\Desktop\\关键词课题\\keywords_location0502.csv",'w',encoding='utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(article_id,art_au_tags,art_all_tags,all_dict))

csvfile.close()








