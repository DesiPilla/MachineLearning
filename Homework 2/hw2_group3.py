# Group 3 Homework 2

import os
import math
import string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

if False:       # Must be True if nltk packages have not been installed yet
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')


def getFiles(path):
    '''
    Input: string (path to directory containing files)
    Output: List of strings (containing paths to each file)
    This function takes a path to a directory and returns a list containing the path to each file in the directory.
    
    Calls: None
    Called by: getData
    '''
    trainingFiles = []
    for root, directories, files in os.walk(path):
        for file in files:
            if '.txt' in file:
                trainingFiles.append(os.path.join(root, file))
    return trainingFiles
      
def getData(directory, filePurpose):
    '''
    Input: string (name of directory containing training files, aka 'dataset 1/'), string ('train' or 'test')
    Output: dictionary {'ham' : hamTrainingFiles, 'spam' : spamTrainingFiles }
    This function takes in a directory and file purpose returns a dictionary containing the files in a data set for both classifications.
    
    Calls: getFiles
    Called by: getAccuracy
    '''
    hamPath = directory + '/' + filePurpose + '/ham/'
    spamPath = directory + '/' + filePurpose + '/spam/'
    hamFiles = getFiles(hamPath)
    spamFiles = getFiles(spamPath) 
    return {'ham' : hamFiles, 'spam' : spamFiles }
      
def getTokens(file):
    '''
    Input: String (path to a file)
    Output: List of strings (terms)
    This function takes a file and returns a list of each token in the file.
        - All punctuation and numbers are removed.
        - All stop words are removed.
        - All terms are converted to lower case.
        - All terms are converted to their root form.
    
    Calls: None
    Called by: getTermCounts
    '''
    # Read and tokenize text
    file = open(file, encoding="ANSI")                                  # Open file
    text = file.read()                                                  # Read in text
    file.close()                                                        # Close the file
    text = text.translate(str.maketrans('', '', string.punctuation))    # Remove punctuation
    tokens = nltk.word_tokenize(text)                                   # Tokenize the text
    
    # Remove tokens that are not alphabetic or stop words
    stopWords = set(stopwords.words('english'))         # Get list of stop words
    terms = []
    for word in tokens:
        if word.isalpha() and (word not in stopWords):
            word = word.lower()                         # Convert word to lower case
            word = wn.morphy(word)                      # Convert word to its stem
            terms.append(word)                          # Add stemmed word to words
    return terms

def getTermGivenClass(term, setTerms):
    '''
    Inputs: string (term), dictionary {term : count}
    Output: float ( P[term|class] )
    This function takes in a term and a dictionary of all terms and divides the number of occurrences of term by the total number of occurrences in the dictionary.
    
    Calls: None
    Called by: getClassGivenTerms
    '''
    try:
        numOccurrences = setTerms[term]
    except:
        numOccurrences = 0
    return (numOccurrences + 1) / (sum(setTerms.values()) + len(setTerms))
    
def getClassGivenTerms(terms, setTerms, pClass):
    '''
    Inputs: string (terms), dictionary {term : count}, float (probability of an instance being of this class)
    Output: float (   log10( P[class|terms] )   )
    This function takes in all of the relevant terms in a file and a dictionary of all terms in a class and returns the logarithm of the probability that the file is classified as such given the file text.
    
    Calls: getTermGivenClass
    Called by: getClass
    '''
    probability = math.log10(pClass)
    for term in terms:
        probability += math.log10(getTermGivenClass(term, setTerms))
    return probability
   
def getTermCounts(classes):
    '''
    Input: dictionary {'ham' : hamTrainingFiles, 'spam' : spamTrainingFiles }
    Output: dictionary {'ham' : {term : count},    'spam' : {term : count} }
    This function returns a 2D dictionary. 
    The dictionary contains two sub-dictionaries.
    Each sub-dictionary contains every term in the classification and the number of times they occurred.
    
    Calls: getTokens
    Called by: getAccuracy
    '''
    terms = {}
    for trainingSet in classes:
        # Collect a dictionary of every term in all files and how often they occur
        setTerms = {}
        for file in classes[trainingSet]:
            words = getTokens(file)   
            for term in words:
                if term in setTerms:
                    setTerms[term] += 1
                else: 
                    setTerms[term] = 1
        print("All %s files have been parsed." % "training")
        terms[trainingSet] = setTerms 
    return terms

def getClass(file, classes, setTerms):
    '''
    Input: string (path to file), dictionary {'ham' : {term : count},    'spam' : {term : count} }
    Output: string (classification)
    This function takes in a file and returns the most likely classification of the file.
    A 1 means the file is classified as spam.
    A 0 means the file is not classified as spam (and it thus classified as ham).
    
    Calls: getClassGivenTerms
    Called by: getAccuracy
    '''
    tokens = getTokens(file)            # Get tokens in file
    
    nHam = len(classes['ham'])          # Find the number of ham files there are in the training data
    nSpam = len(classes['spam'])        # Find the number of spam files there are in the training data
    pHam = nHam / (nHam + nSpam)        # Find the probability that a file is of class 'ham'
    pSpam = 1 - pHam                    # Find the probability that a file is of class 'SPam'
    
    cpHam = getClassGivenTerms(tokens, setTerms['ham'], pHam)    # Get conditional probability that the file is of class 'ham'
    cpSpam = getClassGivenTerms(tokens, setTerms['spam'], pSpam) # Get conditional probability that the file is of class 'spam'
    
    if cpSpam > cpHam:
        return 1
    else:
        return 0
    
    
def getAccuracy(dataSetDirectory, filePurpose):
    '''
    Input: string (name of directory of the dataset), string ('test' or 'train')
    Output: None (prints the accurracy of the model)
    
    Calls: getData, getTermCounts, getClass
    Called by: None
    '''
    files = getData(dataSetDirectory, filePurpose)
    print("Getting training files for each class")
    trainClasses = getData(dataSetDirectory, 'train')
    print("\nGetting testing files for each class")
    testClasses = getData(dataSetDirectory, filePurpose)
    print("\nCounting the number of occurrences of each term in the training data")
    trainTerms = getTermCounts(trainClasses)
    print("\nCounting the number of occurrences of each term in the test data")
    testTerms = getTermCounts(testClasses)
    
    nCorrect = 0
    nIncorrect = 0
    print("\nBeginning to check classification accuracy of ham files")
    for file in files['ham']:
        if getClass(file, trainClasses, trainTerms) == 0:
            nCorrect += 1
        else:
            nIncorrect += 1
        
    print("\nBeginning to check classification accuracy of spam files")    
    for file in files['spam']:
        if getClass(file, trainClasses, trainTerms) == 1:
            nCorrect += 1
        else:
            nIncorrect += 0
    print("\nThis model had %.2f %% accuracy on the data." % (nCorrect / (nCorrect + nIncorrect) * 100))


''' 
Call this model as follows:

>>> getAccuracy('dataset 3', 'train')     # Should be 100% accurate
>>> getAccuracy('dataset 1', 'test')      # Will print the accuracy of the model on the test data

If the 'train' and 'test' files are in subfolders, call the model as follows:

>>> getAccuracy('dataset 3/sub1/sub2', 'train')     # Should be 100% accurate
>>> getAccuracy('dataset 1/sub1/sub2', 'test')      # Will print the accuracy of the model on the test data
'''