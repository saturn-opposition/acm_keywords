import csv
import pymysql
import matplotlib.pyplot as plt
import nltk.data
from nltk.tokenize import WordPunctTokenizer
# with open("F:\\acm_data\\title_percentage.csv","r") as csvfile:
#     reader = csv.reader(csvfile)
#     column = [row[2] for row in reader]
# csvfile.close()
# keywords_from_title = []
# for i in range(1,len(column)):
#     keywords_from_title.append(column[i])
#
# with open("F:\\acm_data\\abstract_keyword.csv",'r') as csvfile2:
#     reader2 = csv.reader(csvfile2)
#     column2 = [row[4] for row in reader2]
# csvfile2.close()
# keywords_from_abstract = []
#
# for i in range(1,len(column2)):
#     keywords_from_abstract.append(column2[i])
#
# print(len(keywords_from_abstract))
# print(len(keywords_from_title))
#有些文章有摘要，有些文章没有，所以长度不一样
abstract = []
keywords=[]
article_id=[]
title=[]
def Get_data_in_sql():
    conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article')
    cur=conn.cursor()
    cur.execute('select distinct art_abstract,art_au_tags,article_id,art_title from acm_article where art_abstract != "" and art_au_tags !=""')
    r=cur.fetchall()
    for r1 in r:
        abstract.append(r1[0])
        keywords.append(r1[1])
        article_id.append(r1[2])
        title.append(r1[3])
    conn.close()
    return abstract ,keywords,article_id,title

abstract,keywords,article_id,title = Get_data_in_sql()

for i in range(len(keywords)):
        keywords[i] = keywords[i].split(";")

keyword_from_title = []
keyword_from_abstract = []

for i in range(len(abstract)):
    temp = []
    for word in keywords[i]:
        if word in abstract[i]:
            temp.append(word)
    keyword_from_abstract.append(temp)

for i in range(len(title)):
    temp = []
    for word in keywords[i]:
        if word in title[i]:
            temp.append(word)
    keyword_from_title.append(temp)


combine_keywords = []
for i in range(len(keyword_from_abstract)):
    temp = []
    temp = keyword_from_abstract[i]

    temp.extend(keyword_from_title[i])
    temp = set(temp)
    temp = list(temp)
    combine_keywords.append(temp)

proportion = []
for i in range(len(keywords)):
    temp = len(combine_keywords[i])/len(keywords[i])
    proportion.append(temp)


header = ['article_id','keywords from title','keywords from abstract','proportion']
csvrow1 = article_id
csvrow2 = keyword_from_title
csvrow3 = keyword_from_abstract

with open("C:\\Users\\hjn\\Desktop\\关键词课题\\combine_keyword.csv",'w',encoding='utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(csvrow1,csvrow2,csvrow3,proportion))

csvfile.close()

print("文件生成成功")
# p=[0,0,0,0,0,0]
#
# for i in proportion:
#     if i == 0:
#         p[0] = p[0]+1
#
#     elif i - 0.25 <=0:
#         p[1] = p[1]+1
#     elif i - 0.5 <=0:
#         p[2] = p[2]+1
#     elif i - 0.75 <=0:
#         p[3] = p[3]+1
#     elif i - 1 <0:
#         p[4] = p[4]+1
#     else:
#         p[5] = p[5]+1
#
# print(p)

# labels = 'p=0','(0,0.25]','(0.25,0.5]','(0.5,0.75]','(0.75,1)','p=1'
# size = [p[0],p[1],p[2],p[3],p[4],p[5]]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','purple']
# explode = (0.1, 0, 0, 0,0,0.1)
# plt.pie(size, explode=explode, labels=labels, colors=colors,
#   autopct='%1.1f%%', shadow=True, startangle=90)
# plt.axis('equal')
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\combine_keyword.png")
# plt.show()

