import matplotlib.pyplot as plt
import pymysql
import nltk
import nltk.data
from nltk.tokenize import WordPunctTokenizer
import csv
import pandas as pd
from pandas import DataFrame
def Get_data_in_sql():
    conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article')
    cur=conn.cursor()
    cur.execute('select distinct art_abstract,art_au_tags,article_id from acm_article where art_abstract != "" and art_au_tags !=""')
    r=cur.fetchall()
    for r1 in r:
        abstract.append(r1[0])
        keywords.append(r1[1])
        article_id.append(r1[2])
    conn.close()
    return abstract ,keywords

print("数据库读取数据完毕")
def cut(abstract):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(abstract)
    wordslist = []
    for s in sentences:
        words = WordPunctTokenizer().tokenize(s)
        wordslist.extend(words)
    b = set(wordslist)
    wordsdict = {}
    for each_b in b:
        count = 0
        for word in wordslist:
            if each_b == word:
                count = count + 1
        wordsdict[each_b] = count
    return wordsdict

print("\n\n摘要分词完毕")

abstract=[]
keywords=[]
article_id=[]
article_id=[]
cut_abstract = []
abstract_keywords = []
abstract,keywords = Get_data_in_sql()
for i in range(len(abstract)):
    cut_abstract.append(cut(abstract[i]))
    # print(cut_abstract[i])
    # print('\n')
for i in range(len(keywords)):
    keywords[i] = keywords[i].split(";")




    header = ['article_id','contain keywords','number of occurances','num_occur proportion']
    csvrow1 = article_id
    csvrow2 = []
    csvrow3 = []
    csvrow4 = []

for i in range(len(cut_abstract)):
    temp = []
    count = 0
    percentage = 0
    weight = 0
    for word in keywords[i]:
        if word in cut_abstract[i].keys():
            count = count + 1
            weight = weight + cut_abstract[i][word]
            temp.append(word)
    percentage = round(count/len(keywords[i]),2)
    csvrow2.append(percentage)
    csvrow3.append(weight)
    csvrow4.append(round(weight/len(keywords[i]),2))
    abstract_keywords.append(temp)

with open("C:\\Users\\hjn\\Desktop\\关键词课题\\abstract_keyword.csv",'w',encoding = 'utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(csvrow1 ,csvrow2 ,csvrow3 ,csvrow4,abstract_keywords))
csvfile.close()
#
# p=[0,0,0,0,0,0]
#
# print("\n\n打开csv文件读取数据完毕")
#
# for i in csvrow2:
#     if i == 0:
#         p[0] = p[0]+1
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
# labels = 'p=0', '(0,0.25]', '(0.25,0.5]', '(0.5,0.75]', '(0.75,1)', 'p=1'
# size = [p[0], p[1], p[2], p[3], p[4], p[5]]
# print(size)
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'purple']
# explode = (0.1, 0, 0, 0, 0, 0)
# patches, text1, text2 = plt.pie(size, explode=explode, labels=labels, colors=colors,
#                                 autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=2.5, pctdistance=0.6)
# plt.axis('equal')
# plt.legend()
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\abstract_keyword(percentage).png")
# plt.show()

# print(p)
# p=[0,0,0,0,0,0,0]
#
# print("\n\n第一个图作图完毕")
#
# for i in csvrow4:
#     if i == 0:
#         p[0] = p[0]+1
#     elif i - 0.25 <=0:
#         p[1] = p[1]+1
#     elif i - 0.5 <=0:
#         p[2] = p[2]+1
#     elif i - 0.75 <=0:
#         p[3] = p[3]+1
#     elif i - 1 <0:
#         p[4] = p[4]+1
#     elif i > 1:
#         p[6] = p[6]+1
#     else:
#         p[5] = p[5] + 1
# labels = 'p=0','(0,0.25]','(0.25,0.5]','(0.5,0.75]','(0.75,1)','p=1','p>1'
# size = [p[0],p[1],p[2],p[3],p[4],p[5],p[6]]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','purple','red']
# explode = (0.1, 0, 0, 0,0,0,0.1)
# plt.pie(size,explode=explode,labels=labels,colors=colors,
#                                 labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
#                                 startangle = 90,pctdistance = 0.6)
# plt.axis('equal')
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\abstract_keyword(num_occur_proportion).png")
# plt.show()
#
# print(p)
# print("\n\n第二个图作图完毕")
# w = [0,0,0,0]
#
# for i in csvrow3 :
#     if i ==0:
#         w[0] = w[0] + 1
#     elif i<=5:
#         w[1] = w[1] + 1
#     elif i<=10:
#         w[2] = w[2] + 1
#     elif i>10:
#         w[3] = w[3] + 1
# labels = 'w=0','(0,5]','(5,10]','>10'
# size = [w[0],w[1],w[2],w[3]]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
# explode = (0.1, 0, 0, 0.1)
# plt.pie(size, explode=explode, labels=labels, colors=colors,
#   autopct='%1.1f%%', shadow=True, startangle=90)
# plt.axis('equal')
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\abstract_keyword(weight）.png")
# plt.show()
# print(w)
# print("\n\n第三个图作图完毕")
# df = pd.read_csv("C:\\Users\\hjn\\Desktop\\关键词课题\\abstract_keyword.csv")
# df.insert(loc =4,column = 'keywords',value=abstract_keywords)
#
# data_df = pd.DataFrame(df)
# data_df.to_csv("C:\\Users\\hjn\\Desktop\\关键词课题\\abstract_keyword.csv")
