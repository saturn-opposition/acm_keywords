import pymysql
import nltk
import csv
import re
import nltk.data
from nltk.tokenize import WordPunctTokenizer

import  matplotlib.pyplot as plt


abstract = []


with open("C:\\Users\\hjn\\Desktop\\关键词课题\\combine_keyword.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    keyword_row = [row[2] for row in reader if row[2] != '[]']

with open("C:\\Users\\hjn\\Desktop\\关键词课题\\combine_keyword.csv", 'r', encoding='utf-8') as f:
     reader = csv.reader(f)
     id_row = [row[0] for row in reader if row[2] != '[]']

keyword_row.remove('keywords from abstract')
id_row.pop(0)


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab', db='acm_acm_article', use_unicode=True,
                       charset='utf8')
cur = conn.cursor()

for i in range(len(id_row)):
    cur.execute('select  art_abstract from acm_article where article_id = "' + id_row[i] + '"')
    r = cur.fetchall()
    for rl in r:
        if rl[0] not in abstract :

            abstract.append(r)


for i in range(len(keyword_row)):
    keyword_row[i] = re.findall(r'\[(.+?)\]', keyword_row[i])
    keyword_row[i] = keyword_row[i][0].split(',')
    for j in range(len(keyword_row[i])):
        keyword_row[i][j] = keyword_row[i][j].replace('\'', '')



mylist = []
mlist = []
def delete_tuple(t):

    for x in t:
        if type(x)==type((1,)) or type(x) == type([]):
            delete_tuple(x)

        elif type(x)==type(''):
            mlist.append(x)
    return mlist
mylist = delete_tuple(abstract)

abstract = mylist
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
loc = []




for i in range(len(keyword_row)):
    temp = []

    for s in range(len(keyword_row[i])):
        temp.append(WordPunctTokenizer().tokenize(keyword_row[i][s]))

    keyword_row[i] =list(set(delete_tuple(temp)))
    mlist = []

    # keyword_row[i] = set(delete_tuple(temp))

print(len(keyword_row[2]))
print(type(keyword_row[2]))
print(len(keyword_row))

for i in range(5):
    print(keyword_row[i])
    print("\n\n\n")
# wordslist = []
# for i in range(len(abstract)):
#     wordslist = []
#     sentences = tokenizer.tokenize(abstract[i])
#     for s in sentences:
#         words = WordPunctTokenizer().tokenize(s)
#         wordslist.extend(words)
#     if i==1:
#         print(wordslist)
#     location = 0
#     count = 0
#
#     for j in range(len(keyword_row[i])):
#
#         for k in range(len(wordslist)):
#             if keyword_row[i][j] == wordslist[k]:
#                 location = location + k + 1
#                 count = count + 1
#     if count ==0:
#         count = 1
#     loc.append((location / len(wordslist)) / count)
#
# header = ['article_id', 'keywords_location']
# with open("C:\\Users\\hjn\\Desktop\\关键词课题\\keywords_location.csv", "w", encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header)
#     csvwriter.writerows(zip(id_row, loc))
# csvfile.close()
#
# x = []
# for i in range(len(abstract)):
#     x.append(i+1)
# print(len(x))
# print(len(loc))
#
# print(loc
#       )
# plt.plot(x, loc)
# plt.title('Position of keywords in Abstracts')
# plt.xlabel('abstract')
# plt.ylabel('position')
# plt.show()
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\keywords_location_linechart.png")
#
# p = [0, 0, 0, 0, 0, 0]
#
# for i in loc:
#     if i == 0:
#         p[0] = p[0] + 1
#     elif i - 0.25 <= 0:
#         p[1] = p[1] + 1
#     elif i - 0.5 <= 0:
#         p[2] = p[2] + 1
#     elif i - 0.75 <= 0:
#         p[3] = p[3] + 1
#     elif i - 1 < 0:
#         p[4] = p[4] + 1
#     else:
#         p[5] = p[5] + 1
#
# labels = 'p=0', '(0,0.25]', '(0.25,0.5]', '(0.5,0.75]', '(0.75,1)', 'p=1'
# size = [p[0], p[1], p[2], p[3], p[4], p[5]]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'purple']
# explode = (0.1, 0, 0, 0, 0, 0.1)
# plt.pie(size,explode=explode,labels=labels,colors=colors,
#                                 labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
#                                 startangle = 90,pctdistance = 0.6)
# plt.axis('equal')
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\keywords_location_pie.png")
# plt.show()
#
#
#
#
#
#
#
