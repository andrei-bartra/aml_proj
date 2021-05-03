# -*- coding: utf-8 -*-
'''
  __________________________________________________________
 |                                                         |
 | "Measuring Political Compatibility with node2vec        |
 |  and moral values scale"                                |
 | Authors: -Andrei Bartra (andreibartra)                  |
 |          -Oscar Noriega (onoriega)                      |
 | Date: May 2021                                          |
 |_________________________________________________________|


 =============================================================================
Main Function:
    Authors: Marc Richardson
    Responsible: Marc Richardson
    Date: March 2020
 =============================================================================
'''

#  ________________________________________
# |                                        |
# |              1: Libraries              |
# |________________________________________|


import os, sys
from emfdscore.scoring import score_docs
#  ________________________________________
# |                                        |
# |              2: Settings               |
# |________________________________________|

wd = os.getcwd()
os.chdir(wd)
sys.path.append(os.chdir(wd))

sys.path.insert(0, './ws')
sys.path.insert(1, './dc')

print('Welcome {}'.format(os.environ['USER']))
if os.environ['USER'] == 'Tato':
    
    OUT_CSV_PATH = '/Users/Tato/Desktop/Advanced ML/Project/transcripts/emfd_out.csv'
    IN_CSV_PATH = '/Users/Tato/Desktop/Advanced ML/Project/transcripts/'
elif os.environ['USER'] == 'andrei':

    OUT_CSV_PATH = r'/mnt/d/Google Drive/U Chicago/8. Q6/AML/Project/data/raw_output/emfd_out_sample.csv'
    IN_CSV_PATH = r'/mnt/d/Google Drive/U Chicago/8. Q6/AML/Project/data/trans_test/'


#  ________________________________________
# |                                        |
# |           3: Local Modules             |
# |________________________________________|


#import ws_rev_scrapper as ws
import emfd as em


#  ________________________________________
# |                                        |
# |          2: Webscrappe Test            |
# |________________________________________|

# Main Function
def main():
    em.data_wrap(IN_CSV_PATH, OUT_CSV_PATH)

if __name__ == '__main__':
    main()


