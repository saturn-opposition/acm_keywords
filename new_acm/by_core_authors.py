# coding=utf8
import pymysql
import nltk
import csv
import numpy
from nltk.tokenize import WordPunctTokenizer
import math
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
for i in range(len(art_au_id)):
    temp = art_au_id[i].split(';')
    for j in range(len(temp)):
        id.append(temp[j])

result = Counter(id)
dict_by_paper_num = {}
print(result)
M = 0.749 * math.sqrt(169)

core_author_id = []
non_core_author = []
for i in range(len(art_au_tags)):
    art_au_tags[i] = art_au_tags[i].split(';')

for author_id, paper_num in result.items():
    if paper_num >= M:
        core_author_id.append(author_id)
    else:
        non_core_author.append(author_id)
print(len(core_author_id))
print(len(non_core_author))
author_id = []
author_type = []
core_abstract_average = []
core_abstract_median = []
core_abstract_standard_deviation = []
core_title_average = []
core_title_median = []
core_title_standard_deviation = []
non_abstract_average = []
non_abstract_median = []
non_abstract_standard_deviation = []
non_title_average = []
non_title_median = []
non_title_standard_deviation = []
all_core_abstract_average = []
all_core_abstract_median = []
all_core_abstract_standard_deviation = []
all_core_title_average = []
all_core_title_median = []
all_core_title_standard_deviation = []
all_non_abstract_average = []
all_non_abstract_median = []
all_non_abstract_standard_deviation = []
all_non_title_average = []
all_non_title_median = []
all_non_title_standard_deviation = []
all_core_abstract_p = []
all_core_title_p = []
all_non_abstract_p = []
all_non_title_p = []
print(art_au_id)
for i in range(len(core_author_id)):
    author_id.append(core_author_id[i])
    author_type.append(('core author'))
    abstract = []
    au_tags = []
    a_title = []
    this_author_abstract_p = []
    this_author_title_p = []

    for t in range(len(art_au_id)):
        if core_author_id[i] in art_au_id[t]:
            abstract.append(art_abstract[t])
            au_tags.append(art_au_tags[t])
            a_title.append(art_title[t])

    for k in range(len(abstract)):

        title = stemmerTool(a_title[k].lower())
        tags = []
        for t in range(len(au_tags[k])):
            tags.append(stemmerTool(au_tags[k][t]))
        abstract_a = stemmerTool(abstract[k])
        count_abstract = 0
        count_title = 0

        for t in range(len(tags)):
            if tags[t] in abstract_a:
                count_abstract = count_abstract + 1

            if tags[t] in title:
                count_title = count_title + 1

        p_abstract = count_abstract / len(tags)
        p_title = count_title / len(tags)
        this_author_abstract_p.append(p_abstract)
        this_author_title_p.append(p_title)
        all_core_abstract_p.append(p_abstract)
        all_core_title_p.append(p_title)
        print(p_abstract)
        print(p_title)

    average = sum(this_author_abstract_p) / len(this_author_abstract_p)
    core_abstract_average.append(average)
    this_author_abstract_p_sorted = sorted(this_author_abstract_p)
    median = this_author_abstract_p_sorted[int(len(this_author_abstract_p_sorted) / 2)]
    core_abstract_median.append(median)
    standard_deviation = numpy.std(this_author_abstract_p)
    core_abstract_standard_deviation.append(standard_deviation)

    average = sum(this_author_title_p) / len(this_author_title_p)
    this_author_title_p_sorted = sorted(this_author_title_p)
    median = this_author_title_p_sorted[int(len(this_author_title_p_sorted) / 2)]
    standard_deviation = numpy.std(this_author_title_p)
    core_title_average.append(average)
    core_title_median.append(median)
    core_title_standard_deviation.append(standard_deviation)

for i in range(len(non_core_author)):
    author_id.append(non_core_author[i])
    author_type.append(('non-core author'))
    abstract = []
    au_tags = []
    a_title = []
    this_author_abstract_p = []
    this_author_title_p = []

    for t in range(len(art_au_id)):
        if non_core_author[i] in art_au_id[t]:
            abstract.append(art_abstract[t])
            au_tags.append(art_au_tags[t])
            a_title.append(art_title[t])

    for k in range(len(abstract)):
        title = stemmerTool(a_title[k].lower())
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
        this_author_abstract_p.append(p_abstract)
        this_author_title_p.append(p_title)
        all_non_abstract_p.append(p_abstract)
        all_non_title_p.append(p_title)

    average = sum(this_author_abstract_p) / len(this_author_abstract_p)
    non_abstract_average.append(average)
    this_author_abstract_p_sorted = sorted(this_author_abstract_p)
    median = this_author_abstract_p_sorted[int(len(this_author_abstract_p_sorted) / 2)]
    non_abstract_median.append(median)
    standard_deviation = numpy.std(this_author_abstract_p)
    non_abstract_standard_deviation.append(standard_deviation)

    average = sum(this_author_title_p) / len(this_author_title_p)
    non_title_average.append(average)
    this_author_title_p_sorted = sorted(this_author_title_p)
    median = this_author_title_p_sorted[int(len(this_author_title_p_sorted) / 2)]
    non_title_median.append(median)
    standard_deviation = numpy.std(this_author_title_p)
    non_title_standard_deviation.append(standard_deviation)

average = sum(all_core_abstract_p) / len(all_core_abstract_p)

all_core_abstract_p_sorted = sorted(all_core_abstract_p)
median = all_core_abstract_p_sorted[int(len(all_core_abstract_p_sorted) / 2)]

standard_deviation = numpy.std(all_core_abstract_p)
print("所有核心作者摘要的平均值为" + str(average) + "，中位数为" + str(median) + "，标准差为" + str(standard_deviation))

average = sum(all_core_title_p) / len(all_core_title_p)

all_core_title_p_sorted = sorted(all_core_title_p)
median = all_core_title_p_sorted[int(len(all_core_title_p_sorted) / 2)]

standard_deviation = numpy.std(all_core_title_p)
print("所有核心作者标题的平均值为" + str(average) + "，中位数为" + str(median) + "，标准差为" + str(standard_deviation))

average = sum(all_non_abstract_p) / len(all_non_abstract_p)

all_non_abstract_p_sorted = sorted(all_non_abstract_p)
median = all_non_abstract_p_sorted[int(len(all_non_abstract_p_sorted) / 2)]

standard_deviation = numpy.std(all_non_abstract_p)
print("所有非核心作者摘要的平均值为" + str(average) + "，中位数为" + str(median) + "，标准差为" + str(standard_deviation))

average = sum(all_non_title_p) / len(all_non_title_p)

all_non_title_p_sorted = sorted(all_non_title_p)
median = all_non_abstract_p_sorted[int(len(all_non_title_p_sorted) / 2)]

standard_deviation = numpy.std(all_non_abstract_p)
print("所有非核心作者标题的平均值为" + str(average) + "，中位数为" + str(median) + "，标准差为" + str(standard_deviation))

header = ['author_id', 'abstract_average', 'abstract_median', 'abstract_standard_deviation', 'title_average',
          'title_median', 'title_standard_median']

with open("core_author.csv", 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(core_author_id, core_abstract_average, core_title_median, core_abstract_standard_deviation,
                            core_title_average, core_title_median, core_title_standard_deviation
                            ))

header = ['author_id', 'abstract_average', 'abstract_median', 'abstract_standard_deviation', 'title_average',
          'title_median', 'title_standard_median']
with open("non_author.csv", 'w', encoding='utf-8', newline='') as csvfile2:
    csvwriter = csv.writer(csvfile2)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(non_core_author, non_abstract_average, non_abstract_median, non_abstract_standard_deviation,
                            non_title_average, non_title_median, non_title_standard_deviation
                            ))
csvfile2.close()
