import csv
import nltk.data
from nltk.tokenize import WordPunctTokenizer
import re

def analyze(file_loc,output_frequency_file):
    article_id = []
    title = []
    abstract = []
    keywords = []

    with open(file_loc,"r") as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
        article_id = [row[0] for row in rows]
        title = [row[4] for row in rows]
        abstract = [row[5] for row in rows]
        keywords = [row[13] for row in rows]
    csvfile.close()
    print(len(article_id),len(title),len(abstract),len(keywords))

    words = []
    for i in range(len(keywords)):
            keywords[i] = keywords[i].split(";")
            for j in range(len(keywords[i])):
                words.append(keywords[i][j])


    for s in title:
        temp = WordPunctTokenizer().tokenize(s)
        for w in temp:
            words.append(w)

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for i in range(len(abstract)):
        sentences = tokenizer.tokenize(abstract[i])
        for s in sentences:
            temp = WordPunctTokenizer().tokenize(s)
            for w in temp:
                words.append(w)

    words_dict = {}
    count = 0
    stop_words_file = open(r"C:\Users\hjn\Desktop\关键词课题\英文停用词.txt",encoding='utf-8',errors = 'ignore').read()  #去掉英文停用词
    stop_words = re.split('\n',stop_words_file)
    for i in range(len(words)):
        if (words[i] not in stop_words) & (words[i] not in words_dict.keys()):
            words_dict[words[i]] = 1
        if (words[i] not in stop_words) & (words[i] in words_dict.keys()):
            count = words_dict[words[i]]
            words_dict[words[i]] = count + 1





    header = ['words','frequency']
    with open(output_frequency_file,"w",encoding= 'utf-8',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(zip(words_dict.keys(),words_dict.values()))
    print(file_loc+'已完成')
    csvfile.close()

# analyze(r"C:\Users\hjn\Desktop\关键词课题\1990-1995.csv",r"C:\Users\hjn\Desktop\关键词课题\1990-1995_frequency.csv")
# analyze(r"C:\Users\hjn\Desktop\关键词课题\1996-2000.csv",r"C:\Users\hjn\Desktop\关键词课题\1996-2000_frequency.csv")
# analyze(r"C:\Users\hjn\Desktop\关键词课题\2001-2005.csv",r"C:\Users\hjn\Desktop\关键词课题\2001-2005_frequency.csv")
# analyze(r"C:\Users\hjn\Desktop\关键词课题\2006-2010.csv",r"C:\Users\hjn\Desktop\关键词课题\2006-2010_frequency.csv")
# analyze(r"C:\Users\hjn\Desktop\关键词课题\2011-2015.csv",r"C:\Users\hjn\Desktop\关键词课题\2011-2015_frequency.csv")
# analyze(r"C:\Users\hjn\Desktop\关键词课题\2016-2018.csv",r"C:\Users\hjn\Desktop\关键词课题\2016-2018_frequency.csv")