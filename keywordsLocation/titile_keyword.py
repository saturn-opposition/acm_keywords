import matplotlib.pyplot as plt
import pymysql
import csv
import pandas as pd
from pandas import DataFrame
titles=[]
keywords=[]
article_id=[]
def Get_data_in_sql():
    conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article')
    cur=conn.cursor()
    cur.execute('select distinct art_title,art_au_tags,article_id from acm_article where art_au_tags != ""')
    r=cur.fetchall()
    for r1 in r:
        titles.append(r1[0])
        keywords.append(r1[1])
        article_id.append(r1[2])
    conn.close()
    return titles, keywords

def createDictCSV(fileName="", dataDict={}):
    with open(fileName, "w",newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        for k, v in dataDict.items():
            csvWriter.writerow([k,v])
        print("write dict into csv successfully!")
        csvFile.close()


titles,keywords = Get_data_in_sql()

for i in range(len(keywords)):
        keywords[i] = keywords[i].split(";")
dict = {}
t_contain_k = []                                        #存放标题含有百分之几的关键词的数值结果
count = 0
percentage = 0
title_keywords = []
for i in range(len(titles)):
        temp = []
        for w in keywords[i]:
            if w in titles[i]:
                count = count + 1
                temp.append(w)
        percentage = round(count / (len(keywords[i])),2)
        t_contain_k.append(percentage)
        title_keywords.append(temp)
        dict[article_id[i]] = percentage
        percentage = 0
        count = 0
# createDictCSV("F:\\acm_data\\title_percentage.csv",dict)
p=[0,0,0,0,0,0]

for i in t_contain_k:
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
# labels = 'p=0','0<p<=0.25','0.25<p<=0.5','0.5<p<=0.75','0.75<p<1','p=1'
# size = [p[0],p[1],p[2],p[3],p[4],p[5]]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','purple']
# explode = (0.1, 0, 0, 0,0,0)
# plt.pie(size, explode=explode, labels=labels, colors=colors,
#   autopct='%1.1f%%', shadow=True, startangle=90)
# plt.axis('equal')
# plt.savefig("F:\\acm_data\\title_keyword.png")
# plt.show()
#
#
#
# with open("F:\\acm_data\\title_percentage.csv","a+",encoding= 'utf-8',newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for data in title_keywords:
#         csvwriter.writerows(zip(data))
# df = pd.read_csv("F:\\acm_data\\title_percentage.csv",header = None)
# df.insert(loc =2,column = 'keywords',value=title_keywords)
# print(df)
# data_df = pd.DataFrame(df)
# data_df.to_csv("F:\\acm_data\\title_percentage.csv",index=0)
