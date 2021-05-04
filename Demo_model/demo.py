import pandas as pd 
import numpy as np
import seaborn as sns
import re
import os
from matplotlib import pyplot as plt
#from emfdscore.scoring import score_docs
import torch
import torch.nn as nn
import torch.optim as optim
from collections import Counter
from torchtext.vocab import Vocab
from torch.utils.data import DataLoader
import torch.nn.functional as F
import time


#Load emfd output from sample and filter for characters with
#at least 60 interventions in the sample.
df= pd.read_csv('transcripts/emfd_out.csv')
df = df[df['count']>=60]

#Rearrange columns and keep relevan columns
y = df.pop('Y')
df.insert(0, 'Y', y)
data = df.drop(df.loc[:, 'care_sent':'count'].columns, axis = 1)
data.reset_index(inplace=True)
data.drop(['index'], axis = 1, inplace=True)

#Generate Training/Validation/Test datasets
train, valid, test = np.split(data.sample(frac=1, random_state=42), [int(.7*len(data)), int(.9*len(data))])

#Generate dictionary with characters in place of Vocab
Vocab_char = {}
Vocab_char[0] = '<unk>'
i=1
for char in train['Y'].unique():
    Vocab_char[i] = char
    i+=1

def get_key(val):
    for key, value in Vocab_char.items():
         if val == value:
             return key

def preprocess_data(df):
'''
Takes a DF and arrange its rows into a list of tuples
containing the label (character) and the 5 MF probabilities
vector of each interventon in the DF
'''
    rv = []
    records = df.loc[:, 'care_p':'sanctity_p'].to_records(index=False)
    results = list(records)
    for i in range(len(df)):
        rv.append((df['Y'].iloc[i], results[i]))
    return rv

def collate_fn(batch):
    
    speech_mf = []
    labels = []
    
    for b in batch:
        label = get_key(b[0])
        labels.append(label)
        s = [i for i in b[1]]
        speech_mf.append(s)
    speech_mf = torch.tensor(speech_mf)
    labels = torch.tensor(labels)
    
    return labels, speech_mf


num_labels = len(Vocab_char)
vocab_size = 5

#Simplest NN model definition for demostration purposes
class NNeMFDTagger(nn.Module):
    def __init__(self, num_labels, vocab_size):

        super(NNeMFDTagger, self).__init__()
        self.linear = nn.Linear(vocab_size, num_labels)


    def forward(self, vec):
        return F.log_softmax(self.linear(vec), dim=1)

loss_function = torch.nn.NLLLoss()

def train_an_epoch(dataloader):
    model.train()
    log_interval = 500

    for idx, (label, speech_mf) in enumerate(dataloader):
        model.zero_grad()
        probs = model(speech_mf.float())
        loss = loss_function(probs, label)
        loss.backward()
        optimizer.step()
        if idx % log_interval == 0 and idx > 0:
            print(f'At iteration {idx} the loss is {loss:.3f}.')


def get_accuracy(dataloader):
    model.eval()
    with torch.no_grad():    
        total_acc, total_count = 0, 0
        for idx, (label, speech_mf) in enumerate(dataloader):
            log_probs = model(speech_mf.float())
            total_acc += (log_probs.argmax(1) == label).sum().item()
            total_count += label.size(0)
    return total_acc/total_count


BATCH_SIZE = 64 

#Generate datasets for PyTorch and DataLoaders
train_data = preprocess_data(train)
valid_data = preprocess_data(valid)
test_data = preprocess_data(test)

train_dataloader = DataLoader(train_data, batch_size=BATCH_SIZE,
                              shuffle=True, 
                              collate_fn=collate_fn)
valid_dataloader = DataLoader(valid_data, batch_size=BATCH_SIZE,
                              shuffle=False, 
                              collate_fn=collate_fn)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE,
                             shuffle=False, 
                             collate_fn=collate_fn)

model = NNeMFDTagger(len(Vocab_char),5)

EPOCHS = 6 # epoch
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

accuracies=[]
for epoch in range(1, EPOCHS + 1):
    epoch_start_time = time.time()
    train_an_epoch(train_dataloader)
    accuracy = get_accuracy(valid_dataloader)
    accuracies.append(accuracy)
    time_taken = time.time() - epoch_start_time
    print(f'Epoch: {epoch}, time taken: {time_taken:.1f}s, validation accuracy: {accuracy:.3f}.')
    
plt.plot(range(1, EPOCHS+1), accuracies)