#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 17:30:53 2018

@author: subramanianiyer
"""
import pandas as pd
import numpy as np
from copy import deepcopy
import json
import wget
import zipfile
import os
import pickle
import shutil
from pymongo import MongoClient
pat_client = MongoClient()
df = pd.read_json('p1976.json')
pats_col = pat_client.pat_db.pat_col2
for qrx in df['urls']:
    for tuv in qrx:
        try:
            wget.download(tuv, 'cweek.zip')
            zip_ref = zipfile.ZipFile('cweek.zip', 'r')
            zip_ref.extractall('cweek')
            zip_ref.close()
            try:
                with open('cweek/'+tuv[-23:-3]+'txt') as file:
                    data = file.readlines()
            except:
                os.remove('cweek.zip')
                shutil.rmtree('cweek')
                continue
            giant = ''.join(data)
            os.remove('cweek/'+tuv[-23:-3]+'txt')
            os.rmdir('cweek')
            os.remove('cweek.zip')
            patents = giant.split('PATN\n')[1:]
        except:
            continue
        for patent in patents:
            d = {}
            try:
                d['pno'] = patent.split('PNO  ')[1].split('\n')[0]
            except:
                continue
                
            try:
                d['title'] = patent.split('TTL ')[1].split('\n')[0]
            except:
                continue
                
            d['assg'] = []
            try:
                for i in patent.split('ASSG\nNAM  ')[1:]:
                    d['assg'].append(i.split('\n')[0])
            except:
                continue
                
            try:
                d['art'] = patent.split('ART ')[1].split('\n')[0]
            except:
                continue
                
            d['inv'] = []
            try:
                for i in patent.split('INVT\nNAM ')[1:]:
                    d['inv'].append(i.split('\n')[0])
            except:
                continue
                
            d['urefs'] = []
            try:
                for i in patent.split('UREF\nPNO  ')[1:]:
                    d['urefs'].append(i.split('\n')[0])
            except:
                continue
                
            try:
                d['APD'] = int(patent.split('APD  ')[1].split('\n')[0])
            except:
                continue
                
            try:
                abstPlus = ''.join(patent.split('ABST\n')[1]).split('\n')
            except:
                continue
                
            try:
                ablines = []
                a = 0
                b = True
                while(b and a<len(abstPlus) and a<100):
                    ablines.append(abstPlus[a])
                    a+=1
                    if(abstPlus[a][0]!=' '):
                        b = False
                for i in range(len(ablines)):
                    ablines[i] = ablines[i].strip()
                d['abst'] = ' '.join(ablines)[5::]
            except:
                continue
            
            try:
                bsumPlus =[]
                if(len(patent.split('BSUM\n'))>1):
                    bsumPlus = ''.join(patent.split('BSUM\n')[1]).split('\n')
                bslines = []
                a = 0
                b = True
                while(b and a<len(bsumPlus) and a<7000):
                    bslines.append(bsumPlus[a])
                    a+=1
                    if(a==len(bsumPlus)):
                        b = False
                    elif(len(bsumPlus[a])>0 and bsumPlus[a][0]=='D'):
                        b = False
                for i in range(len(bslines)):
                    if len(bslines[i])>5 and bslines[i][0]==' ':
                        bslines[i] = bslines[i][5:]
                bslines = ' '.join(''.join(bslines).split('PAR '))
                d['sum'] = deepcopy(bslines)
            except:
                continue
            
            try:
                claims = patent.split('CLMS\n')[1].split('PAR  ')[1::]
                for i in range(len(claims)):
                    claims[i] = ''.join(claims[i].split('\nNUM  ')[0].split('\n     '))
                    claims[i] = ''.join(claims[i].split('\n     '))
                d['claims'] = deepcopy(claims)
            except:
                continue
            pats_col.insert(d)
        print(tuv)
    print(qrx)
