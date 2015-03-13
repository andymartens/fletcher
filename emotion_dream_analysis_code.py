#python code: analysis of emotions in dreams

import pymongo
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from nltk.corpus import stopwords
import pandas as pd
import seaborn as sns
from collections import defaultdict

#connect to database:
client = pymongo.MongoClient()  #create a MongoClient to the running mongod instance:
db = client.dreams  
dream_wake_collection = db.dream_wake 

#get and clean waking reports:
cursor_wake = dream_wake_collection.find( {'dream_wake': 'Waking'}, {'text':1, '_id':0})
cursor_wake.count()

waking_corpus = [report['text'] for report in cursor_wake]
waking_corpus_clean = [report for report in waking_corpus if len(report) > 150]  

# find reports that have similarities to other reports to find duplicates 
#(cant just use 'set' because duplicates are not exact):
for i in range(len(waking_corpus_clean)):
    remaining_reports = waking_corpus_clean[i+1:]
    for remaining_report in remaining_reports:
        if waking_corpus_clean[i][10:40] in remaining_report:
            print waking_corpus_clean[i], ' index:', i
            print

#get rid of duplicate waking reports:
waking_corpus_clean = [report for report in waking_corpus_clean if report != waking_corpus_clean[0] 
                           and report != waking_corpus_clean[1] and report != waking_corpus_clean[2] 
                           and report != waking_corpus_clean[10] and report != waking_corpus_clean[12]
                           and report != waking_corpus_clean[17] and report != waking_corpus_clean[19]
                           and report != waking_corpus_clean[69] and report != waking_corpus_clean[70]]
                           
                           
