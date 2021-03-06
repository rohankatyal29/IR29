'''
arguments: <precision_bing> <precision_twitter> <query>

Contains the main loop of the application

'''

import json
import sys
import bingclient
import twitterclient
import constants
import parser
import parserTwitter
import constants
import logging
import indexer
import indexerTwitter
import rocchio
import common
import math
import PorterStemmer


#only if run as standalone script (not imported module) does, __name__  attribute defaults to __main__
#assume first arg is <precision> second is <query>
if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

#create all singleton objects
    arglist = sys.argv
    if len(arglist) < 3:
        print "Usage: <precision_bing> <precision_twitter> <query>"
        sys.exit(1) #exit interpreter

    print 'Desired precision@10 for context: {}'.format(arglist[1])
    print 'Desired precision@10 for trends: {}'.format(arglist[2])

    precisionTenTargBing = float(arglist[1])   #must convert string to float
    precisionTenTargTwitter = float(arglist[2])   #must convert string to float
    #'eECeOiLBFOie0G3C03YjoHSqb1aMhEfqk8qe7Xi2YMs='
    #connect to client with key arg[1] and post a query with arg[3], query

    bingClient = bingclient.BingClient(constants.BING_ACCT_KEY)
    twitterClient = twitterclient.TwitterClient(constants.APP_KEY, constants.APP_SECRET, constants.OAUTH_TOKEN, constants.OAUTH_TOKEN_SECRET)
    indexer = indexer.Indexer()
    expandedQueryBing = ' '.join(arglist[3:])
    queryOptimizer = rocchio.RocchioOptimizeQuery(expandedQueryBing)

    firstPass = 1
    precisionAtK = 0.00
    queryWeights = {}

    #while precision at 10 is less than desired amt issue a query, obtain new precision metric, expand query, repeat
    while (precisionAtK < precisionTenTargBing):
        precisionAtK = 0.00 #reset precision each round
        #PROCESS A QUERY

        print 'Parameters'
        print '%-20s= %s' % ("Query", expandedQueryBing)
        print '%-20s= %s' % ("Target Precision", precisionTenTargBing)

        indexer.clearIndex()

        if firstPass == 1:
            resultBing = bingClient.webQuery(expandedQueryBing)
        else:
            resultBing = bingClient.webQuery(expandedQueryBing)

        jsonResult = json.loads(resultBing)  #convert string to json
        #put result into a list of documents
        parsedResult = parser.Parser(jsonResult['d']['results'])
        parsedResult.parser()
        DocumentListBing = parsedResult.getDocList()

        print 'Total number of results: %d' % len(DocumentListBing)

        #to calc precision@10 display documents to user and ask them to categorize as Relevant or Non-Relevant
        print '======================'

        # Reset collections for relevant ad nonrelevant documents
        relevantDocumentsBing = []
        nonrelevantDocumentsBing = []

        for i in range(len(DocumentListBing)):

            DocumentListBing[i]["ID"] = i
            indexer.indexDocument(DocumentListBing[i])

            print 'Result %d' % (i+1)
            print '['
            print '  %-9s: %10s' % ("URL", DocumentListBing[i]["Url"])
            print '  %-9s: %10s' % ("Title", DocumentListBing[i]["Title"])
            print '  %-9s: %10s' % ("Summary", DocumentListBing[i]["Description"])
            print ']'

            print ''
            sys.stdout.write('Relevant (Y/N)? ')
            value = raw_input()
            if value.upper() == 'Y':
                DocumentListBing[i]['IsRelevant'] = 1   #1 is true , 0 is false
                precisionAtK = precisionAtK + 1
                relevantDocumentsBing.append(i)

            elif value.upper() == 'N':
                DocumentListBing[i]['IsRelevant'] = 0   #1 is true , 0 is false
                nonrelevantDocumentsBing.append(i)
            else:
                DocumentListBing[i]['IsRelevant'] = 1   #1 is true , 0 is false
                precisionAtK = precisionAtK + 1
                relevantDocumentsBing.append(i)
                print 'Invalid value entered!'



        precisionAtK = float(precisionAtK) / 10  #final precision@10 per round

        print ''
        print 'Precision@10 is: {}'.format(float(precisionAtK))
        print ''

        #expand query here by indexing and weighting current document list
        if (precisionAtK == 0):
            print 'Below desired precision, but can no longer augment the query'
            sys.exit()

        if precisionAtK < precisionTenTargBing:
            print 'Indexing results...'
            indexer.waitForIndexer() # Will block until indexer is done indexing all documents

        # Print inveretd file

        for term in sorted(indexer.invertedFile, key=lambda posting: len(indexer.invertedFile[posting].keys())):
            logging.info("%-30s %-2s:%-3d %-2s:%-3d %-3s:%-10f" % (term, "TF", indexer.termsFrequencies[term], "DF", len(indexer.invertedFile[term]), "IDF", math.log(float(len(DocumentListBing)) / len(indexer.invertedFile[term].keys()),10)))

        print '======================'
        print 'FEEDBACK SUMMARY'


        if (precisionAtK < precisionTenTargBing):
            print ''
            print 'Still below desired precision of %f' % precisionTenTargBing
            queryWeights = queryOptimizer.Rocchio(indexer.invertedFile, DocumentListBing, relevantDocumentsBing, nonrelevantDocumentsBing)   #optimize new query here
            newTerms = common.getTopTerms(expandedQueryBing, queryWeights, 1)
            #check if there are 2 new terms before adding
            expandedQueryBing = expandedQueryBing + " " + newTerms[0]
            firstPass = 0

            print 'Augmenting by %s' % (newTerms[0])
            print 'Expanded Query: ' + expandedQueryBing
            sys.stdout.write('If you are not satisfied with this expansion, let\'s try and achieve the precision you want. Are you satisfied? (Y/N)? ')
            value = raw_input()
            if value.upper() == 'Y':
                break

    #precision@10 is > desired , return query and results to user
    print 'Desired precision for context reached, done'

    ## CAPTURING TRENDS

    precisionAtK = 0.0

    expandedQueryTwitter = expandedQueryBing
    queryOptimizer.clearQuery(expandedQueryTwitter)
    indexerTwitter = indexerTwitter.Indexer()

    while (precisionAtK < precisionTenTargTwitter):
        precisionAtK = 0.00 #reset precision each round
        #PROCESS A QUERY

        print 'Parameters'
        print '%-20s= %s' % ("Query", expandedQueryTwitter)
        print '%-20s= %s' % ("Target Precision", precisionTenTargTwitter)

        indexerTwitter.clearIndex()
        resultTwitter = twitterClient.webQuery(expandedQueryTwitter)

        # jsonResult = json.loads(resultTwitter)  #convert string to json
        # put result into a list of documents
        parsedResultTwitter = parserTwitter.Parser(resultTwitter)
        parsedResultTwitter.parser()
        DocumentListTwitter = parsedResultTwitter.getDocList()

        print 'Total number of results: %d' % len(DocumentListTwitter)

        #to calc precision@10 display documents to user and ask them to categorize as Relevant or Non-Relevant
        print '======================'

        # Reset collections for relevant ad nonrelevant documents
        relevantDocumentsTwitter = []
        nonrelevantDocumentsTwitter = []

        for i in range(len(DocumentListTwitter)):

            DocumentListTwitter[i]["ID"] = i
            indexerTwitter.indexDocument(DocumentListTwitter[i])

            print 'Result %d' % (i+1)
            print '['
            print '  %-9s: %10s' % ("User Screen Name", DocumentListTwitter[i]['Title'])
            print '  %-9s: %10s' % ("URL", DocumentListTwitter[i]["Url"])
            print '  Tweet Text: ' + DocumentListTwitter[i]['Description']
            print '  Processd Tweet: ' + DocumentListTwitter[i]['ProcessedTweet']
            print '  documentListID: ' + str(DocumentListTwitter[i]['ID'])
            print ']'

            print ''
            sys.stdout.write('Relevant (Y/N)? ')
            value = raw_input()
            if value.upper() == 'Y':
                DocumentListTwitter[i]['IsRelevant'] = 1   #1 is true , 0 is false
                precisionAtK = precisionAtK + 1
                relevantDocumentsTwitter.append(i)

            elif value.upper() == 'N':
                DocumentListTwitter[i]['IsRelevant'] = 0   #1 is true , 0 is false
                nonrelevantDocumentsTwitter.append(i)
            else:
                DocumentListTwitter[i]['IsRelevant'] = 1   #1 is true , 0 is false
                precisionAtK = precisionAtK + 1
                relevantDocumentsTwitter.append(i)
                print 'Invalid value entered!'


        precisionAtK = float(precisionAtK) / 10  #final precision@10 per round

        print ''
        print 'Precision@10 is: {}'.format(float(precisionAtK))
        print ''

        #expand query here by indexing and weighting current document list
        if (precisionAtK == 0):
            print 'Below desired precision, but can no longer augment the query'
            sys.exit()

        print 'Indexing results...'
        indexerTwitter.waitForIndexer() # Will block until indexer is done indexing all documents

        # Print inveretd file

        for term in sorted(indexerTwitter.invertedFile, key=lambda posting: len(indexerTwitter.invertedFile[posting].keys())):
            logging.info("%-30s %-2s:%-3d %-2s:%-3d %-3s:%-10f" % (term, "TF", indexerTwitter.termsFrequencies[term], "DF", len(indexerTwitter.invertedFile[term]), "IDF", math.log(float(len(DocumentListTwitter)) / len(indexerTwitter.invertedFile[term].keys()),10)))

        print '======================'
        print 'FEEDBACK SUMMARY'


        if (precisionAtK < precisionTenTargTwitter):
            print ''
            print 'Still below desired precision of %f' % precisionTenTargTwitter

            queryWeights = queryOptimizer.Rocchio(indexerTwitter.invertedFile, DocumentListTwitter, relevantDocumentsTwitter, nonrelevantDocumentsTwitter)   #optimize new query here

            newTerms = common.getTopTerms(expandedQueryTwitter, queryWeights, 1)
            expandedQueryTwitter = expandedQueryTwitter + " " + newTerms[0]

            print 'Augmenting by %s' % (newTerms[0])

    queryWeights = queryOptimizer.Rocchio(indexerTwitter.invertedFile, DocumentListTwitter, relevantDocumentsTwitter, nonrelevantDocumentsTwitter)   #optimize new query here

    newTerms = common.getTopTerms(expandedQueryTwitter, queryWeights, 1)
    expandedQueryTwitter = expandedQueryTwitter + " " + newTerms[0]
    print 'Found trend: ' + newTerms[0]
    #precision@10 is > desired , return query and results to user
    print 'Desired precision for context reached, done'





