import pymysql
import nltk
import csv

import nltk.data

from nltk.stem.porter import PorterStemmer

def stemmerTool(word_data):
    porter_stemmer = PorterStemmer()
    # First Word tokenization
    nltk_tokens = nltk.word_tokenize(word_data)
    # Next find the roots of the word
    words = []
    for w in nltk_tokens:
        words.append(porter_stemmer.stem(w))
    term = ' '.join(words).strip()
    return term


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab', db='acm_keyword', use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
cursor.execute("select article_id,ref_article_id from acm_article_reference ")
row = cursor.fetchall()
article_id = {}
ref_article_id = []
for i in range(len(row)):
    if (row[i][1] ==str(-1)) or (row[i][1][0]=='h'):
        continue
    if row[i][0] in article_id.keys():
        ref_str = article_id[row[i][0]] + ';'+str(row[i][1])
        article_id[row[i][0]] = ref_str
    else:
        article_id[row[i][0]] = str(row[i][1])
article_keywords = {}
article_ref_title = {}
article_ref_keywords = {}
article_ref_title_p = []
article_ref_keywords_p = []
article_ref_abstract_p = []
title_and_abstract = []
for id,ref_id in article_id.items():
    print(id)
    cursor.execute("select art_au_tags from acm_article_final where article_id = \'"+id+'\'')
    row = cursor.fetchall()

    if len(row)==0:
        continue
    keywords = row[0][0]

    ref_id_list = ref_id.split(';')
    ref_title = []
    ref_keywords = []
    ref_abstract = []
    print(ref_id_list)
    for j in range(len(ref_id_list)):
        cursor.execute("select art_title,art_au_tags,art_abstract from acm_article_final where article_id = \'" + ref_id_list[j] + '\'')
        row = cursor.fetchall()

        for t in range(len(row)):
            ref_title.append(stemmerTool(row[t][0]))
            ref_keyword = row[t][1].split(';')
            ref_abstract.append(stemmerTool(row[t][2].lower()))
            for i in range(len(ref_keyword)):
                ref_keywords.append(stemmerTool(ref_keyword[i].lower()))

    if len(ref_keywords)==0:
        continue
    article_ref_title[id] = ';'.join(ref_title)
    article_ref_keywords[id] = ';'.join(ref_keywords)
    keywords = keywords.split(';')
    new_keywords= []
    title_p = 0
    title_count = 0
    keywords_p = 0
    keywords_count = 0
    abstract_count = 0
    abstract_p = 0
    title_abstract_count = 0
    for j in range(len(keywords)):
        new_keywords.append(stemmerTool(keywords[j]))
        this_art_keywords = stemmerTool(keywords[j])
        if this_art_keywords in ref_title:
            title_count = title_count + 1
            if this_art_keywords in ref_abstract:
                title_abstract_count = title_abstract_count + 1
        if this_art_keywords in ref_keywords:
            keywords_count =keywords_count + 1
        if this_art_keywords in ref_abstract:
            abstract_count = abstract_count + 1


    article_keywords[id] = ';'.join(new_keywords)
    title_p = title_count / len(keywords)
    keywords_p = keywords_count/len(keywords)
    abstract_p = abstract_count/len(keywords)
    article_ref_title_p.append(title_p)
    article_ref_keywords_p.append(keywords_p)
    article_ref_abstract_p.append(abstract_p)
    title_and_abstract.append(title_abstract_count/len(keywords))

id = article_id.keys()
header = ['article_id', 'article_keywords', 'ref_keywords', 'ref_title', 'title_p', 'abstract_p','title and abstract','keywords_p']
with open("ref.csv", 'w', encoding='utf-8', newline='') as csvfile2:
    csvwriter = csv.writer(csvfile2)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(id,article_keywords.values(),article_ref_keywords.values(),article_ref_title.values(),article_ref_title_p,article_ref_abstract_p,title_and_abstract,article_ref_keywords_p
                            ))
csvfile2.close()












