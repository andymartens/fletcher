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

#GET AND CLEAN WAKING REPORTS:
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
              
#change all words in waking reports to lowercase
waking_corpus_lower =[]
for report in waking_corpus_clean:
    textblob_report = TextBlob(report)
    waking_report = ' '.join([word.lower() for word in textblob_report.words]) 
    waking_corpus_lower.append(waking_report)  

#corret spelling in waking reports
waking_corpus_spell_correct =[]
for report in waking_corpus_lower:
    textblob_report = TextBlob(report)
    waking_report_spelled = textblob_report.correct()
    waking_corpus_spell_correct.append(waking_report_spelled)  
    

#GET AND CLEAN DREAM REPORTS
cursor_dreams = dream_wake_collection.find( {'dream_wake': 'Dream'}, {'text':1, '_id':0})
dream_corpus = [dream['text'] for dream in cursor_dreams]
dream_corpus_clean = [dream for dream in dream_corpus if len(dream) > 150]  

#find duplicate dreams
for i in range(len(dream_corpus_clean)):
    remaining_dreams = dream_corpus_clean[i+1:]
    for remaining_dream in remaining_dreams:
        if dream_corpus_clean[i][10:30] in remaining_dream:
            print dream_corpus_clean[i], ' index:', i
            print

#get rid of duplicate dreams:
dream_corpus_clean = [dream for dream in dream_corpus_clean if dream != dream_corpus_clean[0] 
                           and dream != dream_corpus_clean[1] and dream != dream_corpus_clean[9] 
                           and dream != dream_corpus_clean[14] and dream != dream_corpus_clean[15]
                           and dream != dream_corpus_clean[16] and dream != dream_corpus_clean[17]
                           and dream != dream_corpus_clean[68] and dream != dream_corpus_clean[69]
                           and dream != dream_corpus_clean[183]]

#change all words in dream reports to lowercase
dream_corpus_lower =[]
for report in dream_corpus_clean:
    textblob_report = TextBlob(report)
    dream_report = ' '.join([word.lower() for word in textblob_report.words]) 
    dream_corpus_lower.append(dream_report)  

#corret spelling in dream reports
dream_corpus_spell_correct =[]
for report in dream_corpus_lower:
    textblob_report = TextBlob(report)
    dream_report_spelled = textblob_report.correct()
    dream_corpus_spell_correct.append(dream_report_spelled)  


#replace all emotion words in waking report corpus with the root word. 
#i.e, replace scare and scary with scared. 
waking_corpus_replaced_emotions = []
for waking_report in waking_corpus_spell_correct:   
    for key in emotions_hierarchy_dict.keys():
        for word in emotions_hierarchy_dict[key]:
            waking_report = waking_report.replace(word, key)
    waking_corpus_replaced_emotions.append(waking_report)
    
#replace all emotion words in dream report corpus with the root word. 
#i.e, replace scare and scary with scared. 
dream_corpus_replaced_emotions = []
for dream_report in dream_corpus_spell_correct:   
    for key in emotions_hierarchy_dict.keys():
        for word in emotions_hierarchy_dict[key]:
            dream_report = dream_report.replace(word, key)
    dream_corpus_replaced_emotions.append(dream_report)



#sort emotions words alphabetically 
def sort_emotion_counts_alphabetically(dictionary):
    """Takes dictionary with each emotion and how many docs it appears in (from a corpus) and sorts the emotions
    (and corresponding counts) from a to z"""
    dream_words_to_counts_list = []
    for key, value in dictionary.iteritems():
        dream_words_to_counts_list.append([key, sum(value)])

    def get_key(item):
        return item[0]

    sorted_emotions_dream_words_to_counts = sorted(dream_words_to_counts_list, key=get_key)
    return sorted_emotions_dream_words_to_counts



#to compute ratio of emotions in dream reports over waking reports
def get_emotion_ratios(dream_emotion_counts_sorted_alphabetically, waking_emotion_counts_sorted_alphabetically):
    """Takes list of emotions and their counts sorted alphabetically and computes emotion ratios.
    Then sorts these emotion ratios from highest to lowest"""

    emotions_ratio_list = [] 
    for i in range(len(dream_emotion_counts_sorted_alphabetically)):
        emotion = dream_emotion_counts_sorted_alphabetically[i][0]
        ratio = float((dream_emotion_counts_sorted_alphabetically[i][1] + 10)) / float((waking_emotion_counts_sorted_alphabetically[i][1] + 10))
        emotions_ratio_list.append([emotion, ratio])

    sorted_emotion_ratios = sorted(emotions_ratio_list, key=get_key, reverse=True)
    return sorted_emotion_ratios


#replace all values with their key in emotions_complete_dict. waking reports
waking_corpus_replaced_emotions_complete = []
for waking_report in waking_corpus_spell_correct:   
    for key in emotion_words_complete_dict.keys():
        for word in emotion_words_complete_dict[key]:
           waking_report = waking_report.replace(word, key)
    waking_corpus_replaced_emotions_complete.append(waking_report)

#replace all values with their key in emotions_complete_dict. dream reports
dream_corpus_replaced_emotions_complete = []
for dream_report in dream_corpus_spell_correct:   
    for key in emotion_words_complete_dict.keys():
        for word in emotion_words_complete_dict[key]:
            dream_report = dream_report.replace(word, key)
    dream_corpus_replaced_emotions_complete.append(dream_report)

#create dict where emotion_complete category is the key and the values are whether absent or present in each report (waking)
waking_emotions_complete_dictionary = defaultdict(list)
for waking_report in waking_corpus_replaced_emotions_complete:   
    for emotion in emotion_words_complete_dict.keys():
        if emotion in waking_report:
            waking_emotions_complete_dictionary[emotion].append(1)
        else:
            waking_emotions_complete_dictionary[emotion].append(0)
            
#create dict where emotion_complete category is the key and the values are whether absent or present in each report (dream)
dream_emotions_complete_dictionary = defaultdict(list)
for dream_report in dream_corpus_replaced_emotions_complete:   
    for emotion in emotion_words_complete_dict.keys():
        if emotion in dream_report:
            dream_emotions_complete_dictionary[emotion].append(1)
        else:
            dream_emotions_complete_dictionary[emotion].append(0)


#compute ratio of emotions in dream reports over dream reports
waking_emotion_complete_counts_sorted_alphabetically = sort_emotion_counts_alphabetically(waking_emotions_complete_dictionary)
dream_emotion_complete_counts_sorted_alphabetically = sort_emotion_counts_alphabetically(dream_emotions_complete_dictionary)

#compute dream words to real-life words ratio
dream_to_wake_emotion_complete_ratios = get_emotion_ratios(dream_emotion_complete_counts_sorted_alphabetically, waking_emotion_complete_counts_sorted_alphabetically)

#plot
X = [word[0] for word in dream_to_wake_emotion_complete_ratios[:25]]
Y = [freq[1] for freq in dream_to_wake_emotion_complete_ratios[:25]]

fig = plt.figure(figsize=(15, 5))  #add this to set resolution: , dpi=100
sns.barplot(x = np.array(range(len(X))), y = np.array(Y))
sns.despine(left=True)
plt.title('Emotion-words Most Representative of Dreams', fontsize=17)
plt.xticks(rotation=75)
plt.xticks(np.array(range(len(X))), np.array(X), rotation=75, fontsize=15)
plt.ylim(1, 3.05)
plt.ylabel("Frequency in dreams relative to real events", fontsize=15)


#compute real-life words to dream words ratio. 
#i.e., compute ratio of emotions in waking reports over dream reports
wake_to_dreams_complete_ratio_list = [] 
for i in range(len(dream_emotion_complete_counts_sorted_alphabetically)):
    emotion = dream_emotion_complete_counts_sorted_alphabetically[i][0]
    ratio = float((waking_emotion_complete_counts_sorted_alphabetically[i][1] + 10)) / float((dream_emotion_complete_counts_sorted_alphabetically[i][1] + 10))
    wake_to_dreams_complete_ratio_list.append([emotion, ratio])

sorted_wake_to_dreams_complete_ratio_list = sorted(wake_to_dreams_complete_ratio_list, key=get_key, reverse=True)

#plot
X = [word[0] for word in sorted_wake_to_dreams_complete_ratio_list[:25]]
Y = [freq[1] for freq in sorted_wake_to_dreams_complete_ratio_list[:25]]

fig = plt.figure(figsize=(15, 5))  #add this to set resolution: , dpi=100
sns.barplot(x = np.array(range(len(X))), y = np.array(Y))
sns.despine(left=True)
plt.title('Emotion-words Most Representative of Real Life', fontsize=17)
plt.xticks(rotation=75)
plt.xticks(np.array(range(len(X))), np.array(X), rotation=75, fontsize=15)
plt.ylim(1, 3.6)
plt.ylabel("Frequency in real events relative to dreams", fontsize=17)





