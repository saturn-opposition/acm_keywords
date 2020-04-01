import pymysql
import nltk
import csv
import numpy
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer

from collections import Counter


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


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='acm_keyword', use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
cursor.execute("select art_au_id,art_abstract,art_au_tags,art_title from acm_article_final ")
row = cursor.fetchall()
art_au_id = []
art_abstract = []
art_au_tags = []
art_title = []

for i in range(len(row)):
    art_au_id.append(row[i][0])
    art_abstract.append(row[i][1])
    art_au_tags.append(row[i][2])
    art_title.append(row[i][3])

id = []
for i in range(len(art_au_tags)):
    art_au_tags[i] = art_au_tags[i].split(';')

for i in range(len(art_au_id)):
    temp = art_au_id[i].split(';')
    for j in range(len(temp)):
        id.append(temp[j])

result = Counter(id)
dict_by_paper_num = {}
print(result)
for author_id, paper_num in result.items():
    id_str = ''
    if paper_num in dict_by_paper_num.keys():
        id_str = dict_by_paper_num[paper_num] + ';' + author_id
        dict_by_paper_num[paper_num] = id_str
    else:
        dict_by_paper_num[paper_num] = author_id

paper_num = list(dict_by_paper_num.keys())

abstract_dict = {}
title_dict = {}
for i in range(len(paper_num)):
    this_num_authors = dict_by_paper_num[paper_num[i]].split(";")
    this_num_abstract_p = []
    this_num_title_p = []
    abstract = []
    au_tags = []
    a_title = []

    for j in range(len(this_num_authors)):
        for t in range(len(art_au_id)):
            if this_num_authors[j] in art_au_id[t]:
                abstract.append(art_abstract[t])
                au_tags.append(art_au_tags[t])
                a_title.append(art_title[t])

        for k in range(len(abstract)):

            title = stemmerTool(a_title[k].lower())
            tags = []
            for t in range(len(au_tags[k])):
                tags.append(stemmerTool(au_tags[k][t]))
            abstract_a = stemmerTool(abstract[k].lower())
            count_abstract = 0
            count_title = 0

            for t in range(len(tags)):
                if tags[t] in abstract_a:
                    count_abstract = count_abstract + 1

                if tags[t] in title:
                    count_title = count_title + 1

            p_abstract = count_abstract / len(tags)
            p_title = count_title / len(tags)
            this_num_abstract_p.append(p_abstract)
            this_num_title_p.append(p_title)

    average = sum(this_num_abstract_p) / len(this_num_abstract_p)
    this_num_abstract_p_sorted = sorted(this_num_abstract_p)
    median = this_num_abstract_p_sorted[int(len(this_num_abstract_p_sorted) / 2)]
    standard_deviation = numpy.std(this_num_abstract_p)
    abstract_dict[paper_num[i]] = (average, median, standard_deviation)

    average = sum(this_num_title_p) / len(this_num_title_p)
    this_num_title_p_sorted = sorted(this_num_title_p)
    median = this_num_title_p_sorted[int(len(this_num_title_p_sorted) / 2)]
    standard_deviation = numpy.std(this_num_title_p)
    title_dict[paper_num[i]] = (average, median, standard_deviation)

abstract_average = []
abstract_median = []
abstract_standard_deviation = []
title_average = []
title_median = []
title_standard_deviation = []

for i in range(len(paper_num)):
    abstract_average.append(abstract_dict[paper_num[i]][0])
    abstract_median.append(abstract_dict[paper_num[i]][1])
    abstract_standard_deviation.append(abstract_dict[paper_num[i]][2])
    title_average.append(title_dict[paper_num[i]][0])
    title_median.append(title_dict[paper_num[i]][1])
    title_standard_deviation.append(title_dict[paper_num[i]][2])
header = ['paper_num', 'abstract_average', 'abstract_median', 'abstract_standard_deviation', 'title_average',
          'title_median', 'title_standard_median']
with open("by_paper_num.csv", 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(
        zip(paper_num, abstract_average, abstract_median, abstract_standard_deviation, title_average, title_median,
            title_standard_deviation))

csvfile.close()






