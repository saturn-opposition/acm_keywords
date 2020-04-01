import pymysql
import csv

article_id = []
ref_article_id = []

def Get_data_in_sql():
    conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab',db='acm_acm_article_reference')
    cur=conn.cursor()
    cur.execute('select article_id,ref_article_id from acm_article_reference where ref_article_id != "-1"')
    r=cur.fetchall()
    for r1 in r:
        article_id.append(r1[0])
        ref_article_id.append(r1[1])

    conn.close()
    return article_id,ref_article_id

article_id,ref_article_id = Get_data_in_sql()
article_id_set = set(article_id)
ref_remove_mark = []
art_remove_mark = []


dict = {}
for i in range(len(article_id)):
    if article_id[i] in dict.keys():

            thelist = dict[article_id[i]]
            if ref_article_id[i].isdigit():
                thelist.append(ref_article_id[i])
            dict[article_id[i]] = thelist


    else:
        if ref_article_id[i].isdigit():
            temp = [ref_article_id[i]]
            dict[article_id[i]] = temp


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab',db='acm_acm_article')
cur = conn.cursor()
dict_art_keywords = {}
delete_keys = []
for k in dict.keys():
    cur.execute('select art_au_tags from acm_article where article_id = "'+k+'"')
    r = cur.fetchall()
    for r1 in r:
        if r1[0] == None:
            delete_keys.append(k)
        else:
            dict_art_keywords[k] = r1[0]

for i in range(len(delete_keys)):
    del dict[delete_keys[i]]

for k in dict_art_keywords.keys():
    temp = dict_art_keywords[k]
    temp = temp.split(';')
    dict_art_keywords[k] = temp

dict_ref_keywords = {}

for k,v in dict.items():
    keywords = []
    for id in v:
        temp = []
        cur.execute('select art_au_tags from acm_article where article_id = "' + id + '"')
        r = cur.fetchall()
        for r1 in r:
           if r1[0] == None:
               pass
           else:
               temp = r1[0].split(";")
               keywords.extend(temp)
    dict_ref_keywords[k] = keywords



dict_not_in_ref = {}
dict_proportion = {}

for k,v in dict_art_keywords.items():
    ref_keywords = dict_ref_keywords[k]
    temp = []
    count = 0
    for w in v:
        if w in ref_keywords:
            count = count +1
        else:
            temp.append(w)
    dict_proportion[k] = round(count/len(v),2)
    dict_not_in_ref[k] = temp

print(dict_not_in_ref)
header = ['article_id','keywords_ref_missed','contain_proportion']
csvrow1 = []
csvrow2 = []
csvrow3 = []
for k in dict.keys():
    csvrow1.append(k)
    csvrow2.append(dict_not_in_ref[k])
    csvrow3.append(dict_proportion[k])
# print(len(article_id))
# print(len(csvrow1))
# print(len(csvrow2))
# print(len(csvrow3))
# print(len(dict_not_in_ref))
# print(len(dict))
# print(len(dict_ref_keywords))
# print(len(dict_art_keywords))
# with open("C:\\Users\\hjn\\Desktop\\关键词课题\\reference_keyword.csv",'w',encoding='utf-8',newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header)
#     csvwriter.writerows(zip(csvrow1,csvrow2,csvrow3))
#
# csvfile.close()

p=[0,0,0,0,0,0]

for i in dict_proportion.values():
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

# labels = 'p=0','(0,0.25]','(0.25,0.5]','(0.5,0.75]','(0.75,1)','p=1'
# size = [p[0],p[1],p[2],p[3],p[4],p[5]]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','purple']
# explode = (0.1, 0, 0, 0,0,0.1)
# plt.pie(size, explode=explode, labels=labels, colors=colors,
#   autopct='%1.1f%%', shadow=True, startangle=90)
# plt.axis('equal')
# plt.savefig("C:\\Users\\hjn\\Desktop\\关键词课题\\reference_keyword.png")
# plt.show()

print(p)