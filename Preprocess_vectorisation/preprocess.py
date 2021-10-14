import csv
import pickle

from inltk.inltk import setup

setup("hi")
#This will give runtime error; check if it displays "done".
from inltk.inltk import tokenize

poems_data_path = '/content/drive/MyDrive/Design_Project_Verselet/pre_processing+vectoristation/data_merged.csv'
# 2 files for stopwords, decide later which one gives better results
stop_words_path = '/content/drive/MyDrive/Design_Project_Verselet/pre_processing+vectoristation/Stopwords/stopwords2.txt'

poems_data = open(poems_data_path,'r',encoding='utf8')
stop_words_file = open(stop_words_path,'r',encoding='utf8')

reader = csv.reader(poems_data, delimiter=',')

stop_words = []
for stop_word in stop_words_file:
	stop_words.append(stop_word)

line_count = 0

all_data = []

for row in reader:
	if (line_count == 0):
		pass
	else:
		tokenized_poem = tokenize(row[4],'hi')
		filtered_poem = [word for word in tokenized_poem if not word in stop_words] 
		all_data.append([row[0],row[1],row[2],row[3],filtered_poem])
	line_count += 1
with open('/content/drive/MyDrive/Design_Project_Verselet/pre_processing+vectoristation/pre_processing/processed_data2.txt', 'wb') as processed_data:
   pickle.dump(all_data, processed_data)
