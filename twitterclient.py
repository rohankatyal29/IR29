from twython import Twython, TwythonError
import json
from pymongo import MongoClient
from nltk.corpus import stopwords
import string
import re
import constants

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class TwitterClient:

    '''
    classdocs
    '''
    def __init__(self, APP_KEY, APP_SECRET , OAUTH_TOKEN , OAUTH_TOKEN_SECRET ):
        '''
        Constructor
        '''
        self.app_key = APP_KEY
        self.app_secret = APP_SECRET
        self.oauth_token = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET

    def webQuery(self, query):

        # Requires Authentication as of Twitter API v1.1
        twitter = Twython(self.app_key, self.app_secret, self.oauth_token, self.oauth_token_secret)

        try:
            #user_timeline = twitter.get_user_timeline(screen_name='meghaarora42')

            # words = re.compile('\w+').findall(query)
            # if len(words) == 1:
            #     expandedQueryTwitter = query
            # else:
            #     expandedQueryTwitter = ' and '.join('"{0}"'.format(w) for w in words)

            print "****** Searching Twitter for: " + query
            user_timeline = twitter.search(q=str(query), count='10')
        except TwythonError as e:
            print e

        #The JSON output object is stored in this file. Go to http://jsonviewer.stack.hu/ and paste the content of this file there. 
        #Then go to viewer tab on the website and view the JSON object 
        f = open('../tweets.txt', 'w')
        f.write(json.dumps(user_timeline))
        f.close()

        # password = ''
        # #Lets put this data in database
        # con = mysql.connect("localhost","igdtuw_user",password,"igdtuw")
        # cur = con.cursor()

        # #create a table for data to be inserted
        # sql_create_table = "CREATE TABLE IF NOT EXISTS Twitter(tweet_id varchar(50), user_id varchar(50), screen_name varchar(50), text varchar(200), is_retweeted varchar(10), retweet_count integer)"
        # cur.execute(sql_create_table)
        # con.commit()

        # client = MongoClient('localhost', 27017)
        # db = client['IR']
        # collection = db['twitter']
    
        #parse the tweets
        #for tweet_item in user_timeline:
        # for tweet_item in user_timeline['statuses']:
        #     # tweet_id = tweet_item['id']
        #     # user_id =  tweet_item['user']['id']
        #     # screen_name = tweet_item['user']['screen_name']
        #     # text =  tweet_item['text']
        #     # tokens = preprocess(text)
        #     # terms_stop = [term for term in tokens if term not in stop]
        #     # is_retweeted =  tweet_item['retweeted']
        #     # retweet_count = tweet_item['retweet_count']
        #     try:
        #         collection.insert(tweet_item)
        #         # print tweet_id , screen_name, text

        #     except: pass

        return user_timeline
    
    

