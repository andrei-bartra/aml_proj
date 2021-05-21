import pandas as pd
import numpy as np
import re, fnmatch
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

#Moral Foundations dictionaries load

#Original Moral Foundations Dictionary
MFD = 'D:\Google Drive\U Chicago\8. Q6\AML\Project\dictionaries\mft_original.dic'
nummap = dict()
mfd = dict()
mfd_regex = dict()
wordmode = True
with open(MFD, 'r') as f:
    for line in f.readlines():
        ent = line.strip().split()
        if line[0] == '%':
            wordmode = not wordmode
        elif len(ent) > 0:
            if wordmode:
                #Use word stems for keys instead of whole word
                wordkey = ent[0].replace("*", "")
                mfd[stemmer.stem(wordkey)] = [nummap[e] for e in ent[1:]]
            else:
                nummap[ent[0]] = ent[1]
                
mfd_foundations = ['care.virtue', 'fairness.virtue', 'loyalty.virtue',
                   'authority.virtue','sanctity.virtue',
                   'care.vice','fairness.vice','loyalty.vice',
                   'authority.vice','sanctity.vice','moral']

for v in mfd.keys():
    mfd_regex[v] = re.compile(fnmatch.translate(v))

    
#Moral Foundations Dictionary '2.0'
MFD2 = 'D:\Google Drive\U Chicago\8. Q6\AML\Project\dictionaries\mfd2.0.dic'
nummap = dict()
mfd2 = dict()
wordmode = True
with open(MFD2, 'r') as f:
    for line in f.readlines():
        ent = line.strip().split()
        if line[0] == '%':
            wordmode = not wordmode
        elif len(ent) > 0:
            if wordmode:
                wordkey = ''.join([e for e in ent if e not in nummap.keys()])
                #Use word stems for keys instead of whole word
                mfd2[stemmer.stem(wordkey)] = [nummap[e] for e in ent if e in nummap.keys()]
            else:
                nummap[ent[0]] = ent[1]

mfd2 = pd.DataFrame.from_dict(mfd2).T
mfd2_foundations = mfd2[0].unique()
mfd2['foundation'] = mfd2[0]
del mfd2[0]
mfd2 = mfd2.T.to_dict()