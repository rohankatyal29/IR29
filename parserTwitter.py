'''
Created on Sep 25, 2012

@author: johnterzis

Parser takes raw json output from BingClient and parses the result list of dictionaries, placing 
significant components into a Document List

e.g.
if json document, exampleResults, is passed into contructor

exampleResults['d]['results'] is list of 10 dictionaries, each a result

'''

import json
from nltk.corpus import stopwords
import string
import re

def processTweet(s):
    temp = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '', s)
    temp = re.sub(r'(\:\w+\:|\<[\/\\]?3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|[\:\;\=B8][\-\^]?[3DOPp\@\$\*\\\)\(\/\|])(?=\s|[\!\.\?]|$)', '', temp)
    return temp

class Parser:
    '''
    classdocs
    '''
    def __init__(self, rawJSON):
        
        self.rawJSON = rawJSON
        self.DocumentsList = []

    def parser(self):
     
        results = self.rawJSON
     
        resultLength = len(results['statuses'])
    
        #generate list of dictionaries one for each doc
        self.DocumentsList = [{'ProcessedTweet': processTweet(results['statuses'][k]['text']), 'Description': results['statuses'][k]['text'], 'Title': results['statuses'][k]['user']['screen_name'],
                          'Url':  "https://twitter.com/statuses/" + str(results['statuses'][k]["id"]), 'IsRelevant': None, 'Body': None, 'URLBody': None} for k in range(resultLength)]

    def getDocList(self):
        
        if self.DocumentsList == None:
            print 'Document List Empty!' 
            return   

        return self.DocumentsList
