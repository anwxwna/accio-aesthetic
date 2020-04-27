#! python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 00:23:07 2018

@author: anwch
"""

import os
import praw
from praw.models import MoreComments
import pandas as pd
import datetime as dt
import urllib
import GoogleScraper
import time
import re

os.chdir('F:\\PythonStuff\\RedditMovieBot')

#clientid 14 chars
#secret=27
with open('F:\\PythonStuff\\RedditMovieBot\\personal_use_script.txt') as file:
    msg=file.read()
    cid=msg[0:14]
    secret=msg[15:42]
    username=msg[43:58]
    pswrd=msg[59:]
    

reddit=praw.Reddit(client_id=cid,
                   client_secret=secret,
                   user_agent='filmtree',
                   username=username,
                   password=pswrd)


dom=reddit.domain('https://www.reddit.com/r/AskReddit/comments/5x2r6b/reddit_what_are_some_must_see_documentaries/')


        
class GetText:
    def __init__(self,filmname,degree):
        self.filmname=filmname
        self.search='Movies like ' + self.filmname
        self.filmsubs=['movies','TrueFilm']
        self.degree=degree
        self.Text={'t_comments':[],
                    's_comments':[],
                   'body':[]}
        
    def GetTextReddit(self):
        movs=[]
        
        for mov in self.filmsubs:
                movs.append(reddit.subreddit(mov))
        
        for m in movs:
            for searcht in m.search(self.search,limit=self.degree):
                self.Text['body'].append(searcht.selftext)
                for comment in searcht.comments:
                    if isinstance(comment,MoreComments):
                        continue
                    self.Text['t_comments'].append(comment.body)
                    for scomment in comment.replies:
                        self.Text['s_comments'].append(scomment.body)
        return self.Text
    
    def GetTextGoogle(self):
        data=[]
        sub=[]
        gsearch=self.search + ' reddit'
        try:
            results = GoogleScraper.scrape_google(gsearch, self.degree, "en")
            for result in results:
                data.append(result)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
        for d in data:
            if urllib.parse.urlsplit(d).netloc == 'www.reddit.com':
                sub.append(reddit.submission(d))
        for subs in sub:
            self.Text['body'].append(subs.selftext)
            for top_c in subs.comments:
                if isinstance(top_c,MoreComments):
                        continue
                self.Text['t_comments'].append(top_c.body)
                for sub_c in top_c:
                    self.Text['s_comments'].append(sub_c.body)
        
        return self.Text
        
    def cleaner(self):
        for key in self.Text.keys():
            for ent in self.Text[key]:
#                print('enenenent',ent)
                re.sub(r"\s","",ent)
                print('#######',ent)
        return self.Text
        
           
                        

red=GetText('Mulholland Drive',2)
red.GetTextReddit()
text=red.cleaner()
#text_df=pd.DataFrame.from_dict(text)
print(text)

#class TextAna:
#    def __init__(self,text):
#        self.text=text
#    
#    def SearchCap():
#        CapReg=re.compile(r'')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
                
        
        
