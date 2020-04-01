import pymysql
import csv
import nltk
from nltk.stem.porter import PorterStemmer

abstracts = []
keywords = []
article_id = []


# 连接数据库，获取相应的数据，并返回摘要和关键词
def get_data_in_sql():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab.', db='acm_keyword')
    cur = conn.cursor()
    cur.execute('select distinct art_abstract,art_au_tags,article_id from acm_article_final where art_au_tags != ""')
    r = cur.fetchmany(100)
    for r1 in r:
        abstracts.append(r1[0])
        keywords.append(r1[1])
        article_id.append(r1[2])
    conn.close()
    return abstracts, keywords


# 将字典保存到excel中
def create_dict_csv(filename="", datadict={}):
    with open(filename, "w", newline='') as csvFile:
        csv_writer = csv.writer(csvFile)
        csv_writer.writerow(["Probability", "Number of papers"])
        for k, v in datadict.items():
            csv_writer.writerow([k, v])
        print("write dict into csv successfully!")
        csvFile.close()


# 词干提取以及大小写处理
def pre(word_data):
    porter_stem = PorterStemmer()
    # 分词
    tokens = nltk.word_tokenize(word_data)
    # 词干提取
    words = []
    for word in tokens:
        words.append(porter_stem.stem(word))
    term = ''.join(words).lower().strip()
    return term


# 获取摘要和关键词数据
abstracts, keywords = get_data_in_sql()
# print(abstracts)
# print(keywords)
keywords_new_hjn = []
for i in range(len(keywords)):
    keywords_new_hjn.append(pre(keywords[i]).split(';'))


for i in range(len(keywords)):
        keywords[i] = keywords[i].split(";")
# print(keywords)


# 对摘要进行词干提取以及大小写处理
abstracts_new = []
for abstract in abstracts:
    term = pre(abstract)
    abstracts_new.append(term)
# print(abstracts_new)


# 对关键词进行词干提取
keywords_new = []
for keyword in keywords:
    keyword_new = []
    for i in keyword:
        keyword_new.append(pre(i))
    keywords_new.append(keyword_new)

header = ['kewords','hjn_keywords']
with open("C:\\Users\\hjn\\Desktop\\关键词课题\\keywords_test.csv",'w',encoding='utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(keywords_new,keywords_new_hjn))

csvfile.close()