# -*- coding: utf-8 -*-
'''
  ________________________________________
 |                                        |
 | Webscrapping of ONPE Website           |
 | Authors: Andrei Batra                  |
 | Date: February, 2020                   |
 |________________________________________|


 =============================================================================
 It just stores nasty looking strings needed for the crawling process.
 =============================================================================
'''

import sys

url = 'https://www.rev.com/blog/transcript-category/political-transcripts/page/109'
if sys.platform.startswith("darwin"):
    driver_path = ("ws/mac/chromedriver")
elif sys.platform.startswith("win32"):
    driver_path = ("ws/win32/chromedriver.exe")
else:
    driver_path = ("ws/linux/chromedriver")


dpath = r'D:\Google Drive\U Chicago\8. Q6\AML\Project\data\transcripts'

xpaths = {'nbar' :(r'//*[@id="fl-main-content"]/div[1]/div[1]/div/div'),
          'grid' :(r'//*[@id="fl-main-content"]/div[1]/div[1]/div/div/div[2]/div/div/div/div/div[1]'),
          'link' :(r'//*[@id="transcription"]/div/div/div/div/div/p[1]/a'),
          'dwld' :(r'//*[@id="root"]/div/div[1]/div/button'),
          'type' :(r'//*[@id="file-type-select"]'),
          'xprt' :(r'/html/body/div[4]/div/div[2]/div/div/div/div[6]/button')}