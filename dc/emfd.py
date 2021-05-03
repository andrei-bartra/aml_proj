# -*- coding: utf-8 -*-
'''
  _____________________________________________
 |                                             |
 | Webscrapping of REV Political Transcripts   |
 | Authors: - Andrei Batra                     |
 | Date: May, 2021                             |
 |_____________________________________________|


 =============================================================================
 Webscrapping of resume data from JNE website:
     https://www.rev.com/blog/transcript-category/political-transcripts/
 =============================================================================
'''


#  ________________________________________
# |                                        |
# |              1: Libraries              |
# |________________________________________|

#Basics
import os, sys

#EMFD 
from emfdscore.scoring import score_docs

#Parallelizatipn
from mpi4py import MPI

#Other libraries
import re
import pandas as pd 

#Local modules
import admin


#  ________________________________________
# |                                        |
# |               2: Settings              |
# |________________________________________|


# Path Settings
os.chdir(admin.wd)
sys.path.append(os.chdir(admin.wd))


#  ________________________________________
# |                                        |
# |             3: Data Loading            |
# |________________________________________|

def file_cleanning(directory, file):
    filename = os.fsdecode(file)
    with open(directory+filename, 'r+') as f:
        text = f.read()
        text = re.sub('	 ', '', text)
        f.seek(0)
        f.write(text)
        f.truncate()


def file2pandas(directory, file, rv):
    raw = pd.read_csv(directory+file, header=None, delimiter = "\t")
    speaker = raw.iloc[::2].reset_index(drop=True)
    speech = raw.iloc[1::2].reset_index(drop=True)
    df = pd.concat([speaker, speech], axis =1).reset_index(drop=True)
    df.columns = ['speaker', 'speech']
    rv = rv.append(df, ignore_index=True)
    return rv


#  ________________________________________
# |                                        |
# |             4: EMFD Features           |
# |________________________________________|


def emfd_feats(df, dict_type='emfd', prob_map='all', score_method='bow', \
               out_metrics='sentiment'): 
    speech = df['speech'].to_frame()
    speech.columns = [0]
    mfd = score_docs(speech, dict_type, prob_map, score_method, out_metrics, len(speech))
    df = df.merge(mfd, left_index=True, right_index=True)
    return df

#  ________________________________________
# |                                        |
# |          5: Parallel Processing        |
# |________________________________________|

def processing(directory):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print("Hello from processor {}".format(rank))
    f_list = os.listdir(directory)

    ini = round(rank*len(f_list)/size)
    end = round((rank + 1)*len(f_list)/size)
    print('Files from {} to {}'.format(ini, end))
    out = pd.DataFrame()
    for file in f_list[ini:end]:
        file_cleanning(directory, file)
        out = file2pandas(directory, file, out)
        
    out['speech'] = out['speech'].astype(str)
    print(out.dtypes)
    print(out.shape)
    out = emfd_feats(out)
    out['speaker'] = out['speaker'].str.replace(r" \(.*\):","")
    out['speech'] = out["speech"].str.replace(r"(\s*\[.*?\].\s*)", " ").str.strip()
    
    result = comm.gather(out, root=0)
    if rank == 0:
        print('Gathered {} dataframes'.format(len(result)))
        output = pd.concat(result, axis=0)
        return output
    else:
        return


#  ________________________________________
# |                                        |
# |                6: Wrapper              |
# |________________________________________|

def data_wrap(input_path, output_file):
    df = processing(input_path)
    if df is not None:
        df.to_csv(output_file)
        return df





'''
#Inputs

DICT_TYPE = 'emfd'
PROB_MAP = 'all'
SCORE_METHOD = 'bow'
OUT_METRICS = 'sentiment'





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
'''