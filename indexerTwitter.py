'''

Indexer for Tweets. Similar to indexer.py but customized for Twitter

'''

import threading
import datetime
import re
import urllib2
import logging
import constants
from PorterStemmer import PorterStemmer
from common import *
from Queue import Queue
from tokenize import tokenize
from threading import Thread

def filter_ascii(s):
    if all(ord(c) < 128 for c in s) == True:
      string = s
      for c in s:
        # only a-z and A-Z for now
        if (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122):
          continue
        else:
          string = string.replace(c, "")
      return string
    return ''

def processToken(word):
	processed_token = ""
	if word[0] == "@" or word[0] == "#":
		processed_token = word + ' ' + word
	else:
		processed_token = filter_ascii(word)
	return processed_token

class Indexer():


	def __init__(self):
		logging.info("Initializing indexer")
		self.ifile_lock = threading.Lock()
		self.documents_queue = Queue()
		self.invertedFile = dict()
		self.termsFrequencies = dict()

		for i in range(constants.NUM_INDEXER_THREADS):
		    worker = Thread(target=self.index, args=(i, self.documents_queue,))
		    worker.setDaemon(True)
		    worker.start()		

	# Enqueues a task in the indexer queue
	def indexDocument(self,document):
		self.documents_queue.put(document)

	def waitForIndexer(self):
		self.documents_queue.join()

	def clearIndex(self):
		with self.ifile_lock:
			self.invertedFile = dict()
			self.termsFrequencies = dict()		

	def index(self, i, q):
		while True:
			logging.info('Indexer-%s: Waiting for next document' % i)
			document = q.get()

			logging.info('Indexer-%s: Indexing document #%s (%s)' % (i, document["ID"], document["Url"]))

			# Create key to hold tf weights
			document["tfVector"] = { }
		
			document["Body"] = document["ProcessedTweet"]

			# Terms List
			terms = []

			# Tokenizer 
			logging.debug('Indexer-%s: Tokenizing document #%s' % (i, document["ID"]))
			tokens = re.compile(constants.DELIMITERS).split(document["Body"])
			logging.debug('Indexer-%s: Found %d tokens' % (i, len(tokens)))
			j = 0

			# Process Tokens
			p = PorterStemmer()
			for token in tokens:

				# Stem Token
				if (constants.STEM_TOKEN):
					logging.debug('Indexer-%s: Stemming token: \'%s\'' % (i, token))
					token = p.stem(token.lower(), 0,len(token)-1)				
				else:
					token = token.lower()

				# Is token eligible to indexed?
				if (token == '' or len(token) <= 3 or len(token) >= 50 or is_number(token)):
					logging.debug('Indexer-%s: Discarding short or empty token \'%s\'' % (i, token))
					continue
				if token in constants.QUERY_SKIP_TERMS:
					continue
				if processToken(token) == "" or processToken(token) == " ":
					continue
				token = processToken(token)
				terms.append(token)
				if token[0] == "@" or token[0] == "#":
					terms.append(token)

				# Insert into invertedFile
				with self.ifile_lock:
					logging.debug('Indexer-%s: Updating postings for token: %s' % (i, token))

					if not token in self.termsFrequencies:
						self.termsFrequencies[token] = 1
					else:
						self.termsFrequencies[token] = self.termsFrequencies[token] + 1

					if not self.invertedFile.has_key(token):
						self.invertedFile[token] = { }

					if not self.invertedFile[token].has_key(document["ID"]):
						self.invertedFile[token][document["ID"]] = { }

					body_postings = []
					if self.invertedFile[token][document["ID"]].has_key("body"):
						body_postings = self.invertedFile[token][document["ID"]]["body"]
						body_postings.append(j)
					else:
						self.invertedFile[token][document["ID"]]["body"] = [j]

					if (token in document["tfVector"]):
						document["tfVector"][token] = document["tfVector"][token] + 1
					else:
						document["tfVector"][token] = 1


				j = j + 1

			logging.info('Indexer-%s: Finished indexing document %s' % (i, document["ID"]))
			q.task_done()

