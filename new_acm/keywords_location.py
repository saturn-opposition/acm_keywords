import pymysql
import nltk
import csv
import re
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import  WordNetLemmatizer
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
def LemmatizerTool(word_data):
    lemmatizer =WordNetLemmatizer()
    # First Word tokenization
    nltk_tokens = nltk.word_tokenize(word_data)
    # Next find the roots of the word
    words = []
    for w in nltk_tokens:
        words.append(lemmatizer.lemmatize(w))
    term = ' '.join(words).strip()
    return term

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab', db='acm_keyword', use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()
cursor.execute("select article_id,art_abstract,art_au_tags from acm_article_final ")
row = cursor.fetchall()
article_id = []
art_abstract = []
art_au_tags = []
occur_times = []
for i in range(len(row)):
   article_id.append(row[i][0])
   art_abstract.append(row[i][1])
   art_au_tags.append(row[i][2])


all_dict = []
for i in range(len(art_au_tags)):
    art_au_tags[i] = art_au_tags[i].split(';')
for i in range(len(art_au_tags)):

    this_art_dict = {}
    abstract = stemmerTool(art_abstract[i].lower())
    tags = []
    for j in range(len(art_au_tags[i])):
        tags.append(stemmerTool(art_au_tags[i][j]))

    # tags = LemmatizerTool(art_au_tags[i].lower())
    # abstract = LemmatizerTool(art_abstract[i].lower())


    # tags = tags_temp.split(';')
    count = 0
    index = 0

    for t in range(len(tags)):

        location = []
        index = abstract.find(tags[t])
        if index != -1:



            while((index!=len(abstract)-1)&(index!=-1)):
                location.append(str(index / len(abstract)))
                index = abstract.find(tags[t],index+1)

        count = count + len(location)
        this_art_dict[tags[t]] = ';'.join(location)
    print(this_art_dict)
       # for j in range(len(words)):
        #     if words[j]==tags[t]:
        #         count = count + 1
        #         if words[j] in this_art_dict.keys():
        #             location = j/len(words)
        #
        #             str = this_art_dict[words[j]] +";"+location.__str__()
        #             this_art_dict[words[j]] = str
        #
        #         else:
        #             location = round(j / len(words), 2)
        #
        #             this_art_dict[words[j]] = location.__str__()
    occur_times.append(count)

    all_dict.append(this_art_dict)



header = ['article_id','tags','location','occur_times']
with open("C:\\Users\\hjn\\Desktop\\关键词课题\\keywords_location0508.csv",'w',encoding='utf-8',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(article_id,art_au_tags,all_dict,occur_times))

csvfile.close()








