'''

Constants and Setting Variables.

NUM_INDEXER_THREADS		: How many indexer worker threads should work concurrently
DELIMITERS 				: RegEx experession to separate (tokenize) words based on
BING_ACCT_KEY			: Bing Account Key required to invoke Bing API
BING_URL				: Prefix to Bing Query API URL
STEM_TOKEN				: Flag indicates whether tokens should be stemmed in the invertedFile or not (useful to experiment around)
ALPHA 					: Weight for previous query vector terms used while computing the expanded query vector (first term in Rocchio Alg.)
BETA 					: Weight for relevant document vector terms used while computing the expanded query vector (second term in Rocchio Alg.)
GAMMA					: Weight for non-relevant document vector terms used while computing the expanded query vector (second term in Rocchio Alg.)
STEM_IN_ROCCHIO			: Flag indicates whether terms should be stemmed before computing summation of their weights for Rocchio formula
IGNORE_TAGS				: A list of HTML tags in which its content must be ignored (e.g. tags that contain only css or javascript code)
QUERY_SKIP_TERMS		: A list of terms that should not be considered in the expanded query even with high scores (e.g. stop words)
'''

APP_KEY = 'FNvw9uGigsXEDByNEJWYFoeIS'
APP_SECRET =  'JwzMsVDRpG7QKN802nNJvqRgTtIYfWVkKafJ3DEvxJq6ar2QaZ'
OAUTH_TOKEN = '180749030-KVaAVMpHHtve5mUOOG4AUIR0tW3owBNn1vT9e02T'
OAUTH_TOKEN_SECRET = 'Sog4UebCOOSu6TbR84IZEohO0rhpRgUrX4QXvHG5azOik'
NUM_INDEXER_THREADS	=	2
DELIMITERS 			= '[\s.,=?!:@<>()\"-;\'&_\\{\\}\\|\\[\\]\\\\]+' # DELIMITERS 			= '\W+'
BING_ACCT_KEY		= 'EEss/QY1BWmE0o0fSsqvzmcsZ+2S/lTTT0xgvAy4Z8s'
BING_URL			= 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Web?'
STEM_TOKEN			= False
ALPHA 				= 1.0
BETA 				= 0.75
GAMMA				= 0.75
STEM_IN_ROCCHIO		= False
IGNORE_TAGS			= ["style", "script"]
QUERY_SKIP_TERMS	= { "about" : True,
"above" : True,
"after" : True,
"again" : True,
"against" : True,
"all" : True,
"am" : True,
"an" : True,
"and" : True,
"any" : True,
"are" : True,
"aren" : True,
"as" : True,
"at" : True,
"be" : True,
"because" : True,
"been" : True,
"before" : True,
"being" : True,
"below" : True,
"between" : True,
"both" : True,
"but" : True,
"by" : True,
"can" : True,
"cannot" : True,
"could" : True,
"couldn" : True,
"did" : True,
"didn" : True,
"do" : True,
"does" : True,
"doesn" : True,
"doing" : True,
"don" : True,
"down" : True,
"during" : True,
"each" : True,
"few" : True,
"for" : True,
"from" : True,
"further" : True,
"had" : True,
"hadn" : True,
"has" : True,
"hasn" : True,
"have" : True,
"haven" : True,
"having" : True,
"he" : True,
"her" : True,
"here" : True,
"here" : True,
"hers" : True,
"herself" : True,
"him" : True,
"himself" : True,
"his" : True,
"how" : True,
"how" : True,
"if" : True,
"in" : True,
"into" : True,
"is" : True,
"isn" : True,
"it" : True,
"its" : True,
"itself" : True,
"let" : True,
"me" : True,
"more" : True,
"most" : True,
"mustn" : True,
"my" : True,
"myself" : True,
"no" : True,
"nor" : True,
"not" : True,
"of" : True,
"off" : True,
"on" : True,
"once" : True,
"only" : True,
"or" : True,
"other" : True,
"ought" : True,
"our" : True,
"ours" : True,
"ourselves" : True,
"out" : True,
"over" : True,
"own" : True,
"same" : True,
"shan" : True,
"she" : True,
"should" : True,
"shouldn" : True,
"so" : True,
"some" : True,
"such" : True,
"than" : True,
"that" : True,
"the" : True,
"their" : True,
"theirs" : True,
"them" : True,
"themselves" : True,
"then" : True,
"there" : True,
"these" : True,
"they" : True,
"this" : True,
"those" : True,
"through" : True,
"to" : True,
"too" : True,
"under" : True,
"until" : True,
"up" : True,
"very" : True,
"was" : True,
"wasn" : True,
"we" : True,
"were" : True,
"weren" : True,
"what" : True,
"when" : True,
"where" : True,
"which" : True,
"while" : True,
"who" : True,
"whom" : True,
"why" : True,
"with" : True,
"would" : True,
"wouldn" : True,
"you" : True,
"your" : True,
"yours" : True,
"yourself" : True,
"yourselves" : True }
