# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:15:03 2020

@author: EliseIronhack
"""


import requests as r
import pandas as pd
import json 


def acquisition_posts() :
    url = f'https://gateway.reddit.com/desktopapi/v1/subreddits/gaming?limit=200'
    headers = """accept: */*
accept-encoding: gzip, deflate, br
accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
content-type: application/x-www-form-urlencoded
origin: https://www.reddit.com
pragma: no-cache
referer: https://www.reddit.com/
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
x-reddaid: R6BMJPEY7PLKRKYB
x-reddit-loid: 000000000066ambv0y.2.1586507619098.Z0FBQUFBQmVrRDFRUXB0d1J4amc5YlVfNHFmNTJKNzFyTkRCaDlyS20yRzEwY0oxcmZMMElSMl80elUxb2tNaDl5TzJmeUdBbkMzSU9KcVRSYlgtOUpzTzl2NFNjRWxoaGV6TmlJaENvdUZyWWpTczJDWjlXcl9RUHl0cG9DallCNm4zdnQzZG9rZS0
x-reddit-session: KIzBcOcpIblvPZCr4Y.0.1586512806612.Z0FBQUFBQmVrRU9tVC1RbllEc1l5Z0Q5LV85UE5KTDF5V2NqTFJBdUZqdXdZdFpsdUZhNTJQTFFOTlhfTGxJWUNrOXRJQ25RS0RtbnpGZGs1Rl83OVQxRzhUOXIxUUZaRllDWkhPMFhQZFA0U1p0cU9hMTNmYVlZRTJKcmxwdDJYaFBTcVp2ZmxGOGM"""
    
    headers = dict([i.split(': ') for i in headers.split('\n')])
    posts = r.get(url, headers = headers).json()
    
    return posts


def get_subreddit_posts(posts):
    post_id = list(posts['posts'].keys()) 
    posts_df = pd.DataFrame()
    
    
    for i in post_id : 
        df = pd.json_normalize(posts['posts'][i])
        posts_df = posts_df.append(df)
        
    posts_df = posts_df.reset_index()
    posts_df = posts_df[['postId', 'title', 'authorId', 'author', 'numComments','score']]
    
    return posts_df




def get_posts_id(posts_df) : 
    #This function could be used for the next steps
    post_lst = list(posts_df.postId)
    return post_lst


def acquisition_comments():
    
    url = f'https://gateway.reddit.com/desktopapi/v1/postcomments/fxrok1?rtj=only&emotes_as_images=true&allow_over18=&include=prefsSubreddit&subredditName=gaming&hasSortParam=false&include_categories=true&onOtherDiscussions=false&depth=3'
    headers = """accept: */*
accept-encoding: gzip, deflate, br
accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
content-type: application/x-www-form-urlencoded
origin: https://www.reddit.com
pragma: no-cache
referer: https://www.reddit.com/
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
x-reddaid: R6BMJPEY7PLKRKYB
x-reddit-loid: 000000000066ambv0y.2.1586507619098.Z0FBQUFBQmVreWVLTW5YaGc4OG9MNnl1azl2SGZPcDd0SVdtTXFmbzNkbXZINVRndDFDdUVlNlctWnFnbGd1OWFrRzFvWUdKSldJQndWVmh1bHNibWtXM19IWDFXanNjWXVuQUk1Ti15cktaeVRNb181cFc2Q1lieHhSVVB2enJmYmI1QWFfWHNEeFY
x-reddit-session: sPHgYo0RqC1iySI4R5.0.1586703238944.Z0FBQUFBQmVreXVHMzMzTjNmbWpqamlSTG1xWmJtQVR6ZXRWRmpyODVUWWJiMWJidU55aTJsdEZTYmYwdGwyT3g1d09QaWJkQnplazJVY29YaFc3UzBfdkp2NC1iMUFCV21ySjZoREYzQjBZNjZBMk9QM3F1ZWxhbGlBUUYzSnNaQ3VWYWYzVDVzOEo"""
    
    headers = dict([i.split(': ') for i in headers.split('\n')])
    comments = r.get(url, headers = headers).json()
    return comments

def get_com_infos(comments) :

    com_lst = list(map(lambda x: {'author':x['author'], 'authorId' : x['authorId'],
                                  'media':x['media']['richtextContent']['document'][0]['c'][0],
                                  'postId':x['postId'], 'subredditId':x['subredditId']},
                       comments['comments'].values())) #author+comment
    com_df = pd.json_normalize(com_lst)
    print(com_df)
    return com_df


def export_df(post_df, com_df):

    post_df.to_csv('data_post_subs.csv')
    com_df.to_csv('data_com.csv')

    
if __name__ == '__main__':
    posts = acquisition_posts()
    posts_df = get_subreddit_posts(posts)
    post_lst = get_posts_id(posts_df)

    comments = acquisition_comments()
    com_df = get_com_infos(comments)
    export_df(posts_df, com_df)