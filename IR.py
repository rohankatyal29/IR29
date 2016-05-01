from twython import Twython, TwythonError
import json
from pymongo import MongoClient
from nltk.corpus import stopwords
import string
import re 

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#This is your Twitter application details
APP_KEY = 'FNvw9uGigsXEDByNEJWYFoeIS'
APP_SECRET =  'JwzMsVDRpG7QKN802nNJvqRgTtIYfWVkKafJ3DEvxJq6ar2QaZ'
OAUTH_TOKEN = '180749030-KVaAVMpHHtve5mUOOG4AUIR0tW3owBNn1vT9e02T'
OAUTH_TOKEN_SECRET = 'Sog4UebCOOSu6TbR84IZEohO0rhpRgUrX4QXvHG5azOik'

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    #user_timeline = twitter.get_user_timeline(screen_name='prateekdewan')
    user_timeline = twitter.search(q='boy', count='1000')
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

client = MongoClient('localhost', 27017)
db = client['IR']
collection = db['twitter']
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']


#parse the tweets
#for tweet_item in user_timeline:
for tweet_item in user_timeline['statuses']:
    tweet_id = tweet_item['id']
    user_id =  tweet_item['user']['id']
    screen_name = tweet_item['user']['screen_name']
    text =  tweet_item['text']
    tokens = preprocess(text)
    terms_stop = [term for term in tokens if term not in stop]
    print terms_stop
    is_retweeted =  tweet_item['retweeted']
    retweet_count = tweet_item['retweet_count']
    
    try:
        collection.insert(tweet_item)
        # print tweet_id , screen_name, text

    except: pass
    
    

