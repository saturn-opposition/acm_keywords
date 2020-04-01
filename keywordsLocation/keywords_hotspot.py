import csv
import pymysql

keywords = []
article_id = []

# conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article')
# cur=conn.cursor()
# cur.execute('select  art_au_tags,article_id from acm_article where art_au_tags !=""')
# r=cur.fetchall()
# for r1 in r:
#     if r1[0] not in keywords:
#         keywords.append(r1[0])
#         article_id.append(r1[1])
# conn.close()
#
# words = []
# frequency = []
# with open(r"C:\Users\hjn\Desktop\关键词课题\2016-2018_frequency.csv","r") as csvfile:
#     reader = csv.reader(csvfile)
#     rows = [row for row in reader]
#     words = [row[0] for row in rows]
#     frequency = [row[1] for row in rows]
# csvfile.close()
#
# with open(r"C:\Users\hjn\Desktop\关键词课题\2016-2018.csv",'r') as csvfile2:
#     reader2 = csv.reader(csvfile2)
#     rows = [row for row in reader2]
#     article_id = [row[0] for row in rows]
#     keywords = [row[13] for row in rows]
# csvfile2.close()
#
#
# words.pop()
# frequency.pop()
# high_frequency = []
# high_frequency_portion = []
# for i in range(len(keywords)):
#     keywords[i] = keywords[i].split(";")
#     count = 0
#     temp = []
#     for j in range(len(keywords[i])):
#         if keywords[i][j] in words[0:round(len(words)*0.05)]:
#             count = count + 1
#             temp.append(keywords[i][j])
#     high_frequency.append(temp)
#     high_frequency_portion.append(count/len(keywords[i]))

def printportion(loc):
    with open(loc,"r",encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
        high_frequency_portion = [row[3] for row in rows]
    csvfile.close()
    high_frequency_portion.pop(0)


    p = [0,0,0,0,0,0]
    for i in high_frequency_portion:
        if float(i) == 0:
            p[0] = p[0]+1
        elif float(i) - 0.25 <=0:
            p[1] = p[1]+1
        elif float(i) - 0.5 <=0:
            p[2] = p[2]+1
        elif float(i) - 0.75 <=0:
            p[3] = p[3]+1
        elif float(i) - 1 <0:
            p[4] = p[4]+1
        else:
            p[5] = p[5]+1

    print(p)
# header = ['article_id','keywords','high frequency','proportion']
# with open("C:\\Users\\hjn\\Desktop\\关键词课题\\2016-2018keyword_frequency.csv",'w',encoding='utf-8',newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header)
#     csvwriter.writerows(zip(article_id,keywords,high_frequency,high_frequency_portion))
#
# csvfile.close()
printportion(r"C:\Users\hjn\Desktop\关键词课题\2016-2018keyword_frequency.csv")
printportion(r"C:\Users\hjn\Desktop\关键词课题\2011-2015keyword_frequency.csv")
printportion(r"C:\Users\hjn\Desktop\关键词课题\2006-2010keyword_frequency.csv")
printportion(r"C:\Users\hjn\Desktop\关键词课题\2001-2005keyword_frequency.csv")
printportion(r"C:\Users\hjn\Desktop\关键词课题\1996-2000keyword_frequency.csv")
printportion(r"C:\Users\hjn\Desktop\关键词课题\1990_1995keyword_frequency.csv")

