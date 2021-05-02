import pandas as pd 
import numpy as np
import seaborn as sns
import re
import os
from matplotlib import pyplot as plt
from emfdscore.scoring import score_docs


DICT_TYPE = 'emfd'
PROB_MAP = 'all'
SCORE_METHOD = 'bow'
OUT_METRICS = 'sentiment'
OUT_CSV_PATH = '/Users/Tato/Desktop/Advanced ML/Project/transcripts/emfd_out.csv'
directory = '/Users/Tato/Desktop/Advanced ML/Project/transcripts/'

df = pd.DataFrame()

for s in os.listdir(directory):
    filename = os.fsdecode(s)
    with open(directory+filename, 'r+') as f:
        text = f.read()
        text = re.sub('	 ', '', text)
        f.seek(0)
        f.write(text)
        f.truncate()
    raw = pd.read_csv(directory+filename, header=None, delimiter = "\t")
    speaker = raw.iloc[::2]
    speaker.reset_index(drop=True, inplace=True)
    speech = raw.iloc[1::2]
    speech.reset_index(drop=True, inplace=True)
    data = speech.merge(speaker, left_index=True, right_index=True)
    num_docs = len(data)    
    mfd = score_docs(speech,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
    data = data.merge(mfd, left_index=True, right_index=True)
    df = df.append(data, ignore_index = True)
    
df['0_y'] = df['0_y'].str.replace(r" \(.*\):","")
df['0_x'] = df["0_x"].str.replace(r"(\s*\[.*?\].\s*)", " ").str.strip()