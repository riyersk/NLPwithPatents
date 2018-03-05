#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:18:10 2018

@author: subramanianiyer
"""
from pymongo import MongoClient
import numpy as np
import pandas as pd
import re
import gensim
import pickle
from nltk.corpus import stopwords
from collections import defaultdict as dd
#from copy import deepcopy
print('imports done')
d = dd(int)
dels =[]
client = MongoClient()
stops = stopwords.words('english')
stops.append(['invention','embodiment','background','summary','pac','par'])
stops.append(['present','improvement','field','novel','new','description'])
stops.append(['iaddend', 'iadd'])
patc = client.pat_db.pat_col
df = pd.DataFrame(list(patc.find({},{'_id':0,'assg':0,'claims':0,'inv':0,'urefs':0,'title':0,'art':0})))
print('dataframe is go')
dates = [int(x) for x in df['APD']]
df.drop([i for i,j in enumerate(dates) if j>20020000], axis = 0, inplace = True)
df.reset_index(inplace=True)
for i in range(len(df)):
    if d[df['pno'][i]]==0:
        d[df['pno'][i]]=1
    else:
        dels.append(i)
df.drop(df.index[dels], inplace = True)
df.reset_index(inplace=True)
dates = [int(x) for x in df['APD']]
pnos = [x for x in df['pno']]
print('dataframe go 2')
#abstracts = df['abst']
summaries = df['sum']
#abstracts = np.asarray([re.sub('[^ A-Za-z]', '',x) for x in abstracts])
#abstracts = np.asarray([[word for word in x.lower().split() if word not in stops] for x in abstracts])
summaries = [re.sub('[^ A-Za-z]', '',x) for x in summaries]
summaries = [[word for word in x.lower().split() if word not in stops] for x in summaries]
del df
print('abstracts and summaries prepared')

class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
              yield gensim.models.doc2vec.TaggedDocument(doc,[self.labels_list[idx]])
#print('abstract model start')
#lababs = LabeledLineSentence(abstracts, pnos)
#abmodel = gensim.models.doc2vec.Doc2Vec(size=300, window=8, min_count=3, alpha = .025, min_alpha = .025, workers=40)
#abmodel.build_vocab(lababs)
#print('abstract model built')
#a = len(abstracts)
#for epoch in range(10):
#    abmodel.train(lababs, total_examples = a, epochs = 1)
#    abmodel.alpha -= 0.002 # decrease the learning rate
#    abmodel.min_alpha = abmodel.alpha # fix the learning rate, no deca
#    abmodel.train(lababs, total_examples = a, epochs = 1)
#print('abstract docs built')
#abmodel.save('abmodel.model')
#print(abmodel.most_similar(pnos[98]))
#print(abstracts[98])
#print('done with abstracts')
print('summaries model start')
labsums = LabeledLineSentence(summaries, pnos)
summodel = gensim.models.doc2vec.Doc2Vec(size=300, window=8, min_count=3, alpha = .025, min_alpha = .025, workers=40)
summodel.build_vocab(labsums)
print('summary model built')
b = len(summaries)
for epoch in range(10):
    summodel.train(labsums, total_examples = b, epochs = 1)
    summodel.alpha -= 0.002 # decrease the learning rate
    summodel.min_alpha = summodel.alpha # fix the learning rate, no deca
    summodel.train(labsums, total_examples = b, epochs = 1)
print('summary docs built')
summodel.save('summodel.model')
#print(summodel.most_similar(pnos[98]))
print('done with summaries')
#print(summaries[98])
with open('dates.pkl', 'wb') as picklefile:
    pickle.dump(dates, picklefile)
with open('pnos.pkl', 'wb') as picklefile2:
    pickle.dump(pnos, picklefile2)
