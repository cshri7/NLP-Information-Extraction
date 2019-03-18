# these are settings for generating phrases and annotating corpora with phrases
phrase_generator = \
    {
     #'input-file': 'data/raw-data/reviews_data.txt.gz',  # data files, can be file or folder
     'input-file': 'data/raw-data/allApt-allWebsite-data.txt.gz',
     #'output-folder': 'data/tagged-data/',  # directory to output tagged corpora
     'output-folder': 'data/allApt-data/',
     # where to store the phrase file? (only needed if dotag=True)
     #'phrase-file': 'top-opinrank-phrases.txt',
     'phrase-file': 'top-APT-phrases.txt',
     'dotag': True,  # do you want to tag your corpora with phrases and generate a new version of it?
     # a list of stop words in your language
     'stop-file': 'stopwords-en.txt',
     # minimum number of occurrence, use 50 for small datasets, 100 for medium
     # sized dataset
     'min-phrase-count': 10
     }
