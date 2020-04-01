import pymysql
import  nltk
import csv
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
import numpy
from nltk.stem.porter import PorterStemmer
def stemmerTool(word_data):
    porter_stemmer = PorterStemmer()
    # First Word tokenization
    nltk_tokens = nltk.word_tokenize(word_data)
    #Next find the roots of the word
    words = []
    for w in nltk_tokens:
        words.append(porter_stemmer.stem(w))
    term = ' '.join(words).strip()
    return term

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab', db='acm_keyword', use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
cursor.execute("select art_pub_year,art_abstract,art_au_tags,art_title from acm_article_final ")
row = cursor.fetchall()
art_pub_year = []
art_abstract = []
art_au_tags = []
art_title = []
for i in range(len(row)):
   art_pub_year.append(row[i][0])
   art_abstract.append(row[i][1])
   art_au_tags.append(row[i][2])
   art_title.append(row[i][3])

year_title_dict = {}
year_abstract_dict = {}
year_tags_num = {}
for i in range(len(art_au_tags)):
    art_au_tags[i] = art_au_tags[i].split(';')

for i in range(len(art_pub_year)):

    tags = []
    title = stemmerTool(art_title[i].lower())
    tags = []
    for j in range(len(art_au_tags[i])):
        tags.append(stemmerTool(art_au_tags[i][j]))
    abstract = stemmerTool(art_abstract[i].lower())
    count_abstract = 0
    count_title = 0

    for t in range(len(tags)):
        if tags[t] in abstract:
            count_abstract = count_abstract + 1

        if tags[t] in title:
            count_title = count_title + 1

    p_abstract = count_abstract/len(tags)
    p_title = count_title/len(tags)


    if art_pub_year[i] in year_title_dict.keys():
                update = year_title_dict[art_pub_year[i]]+';'+str(p_title)
                year_title_dict[art_pub_year[i]] = update
    else:

                year_title_dict[art_pub_year[i]] = str(p_title)
    if art_pub_year[i] in year_abstract_dict.keys():
                update = year_abstract_dict[art_pub_year[i]]+';'+str(p_abstract)
                year_abstract_dict[art_pub_year[i]] = update
    else:

                year_abstract_dict[art_pub_year[i]] = str(p_abstract)


year = []
title = []
abstract = []

for y,n in year_abstract_dict.items():
    n_float = []
    for i in range(len(n.split(';'))):
        n_float.append(float(n.split(';')[i]))
    # print(n_float)
    n_sorted = sorted(n_float)
    average = sum(n_float)/len(n_float)
    median =n_sorted[int(len(n_float)/2)]
    standard_deviation = numpy.std(n_float)
    year.append(y)
    abstract.append((average,median,standard_deviation))
    this_year_title_tuple = year_title_dict[y]
    n_float = []
    for i in range(len(this_year_title_tuple.split(';'))):
        n_float.append(float(this_year_title_tuple.split(';')[i]))
    # print(n_float)
    average = sum(n_float) / len(n_float)
    title_sorted = sorted(n_float)
    median = title_sorted[int(len(n_float) / 2)]
    standard_deviation = numpy.std(n_float)
    title.append((average,median,standard_deviation))
abstract_average = []
abstract_median = []
abstract_standard_deviation = []
title_average = []
title_median = []
title_standard_deviation = []
for i in range(len(year)):
    abstract_average .append(abstract[i][0])
    abstract_median.append(abstract[i][1])
    abstract_standard_deviation.append(abstract[i][2])
    title_average.append(title[i][0])
    title_median.append(title[i][1])
    title_standard_deviation.append(title[i][2])
header = ['year','abstract_average','abstract_median','abstract_standard_deviation','title_average','title_median','title_standard_median']
with open("C:\\Users\\hjn\\Desktop\\关键词课题\\by_year.csv",'w',encoding='utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(year,abstract_average,abstract_median,abstract_standard_deviation,title_average,title_median,title_standard_deviation))

csvfile.close()




