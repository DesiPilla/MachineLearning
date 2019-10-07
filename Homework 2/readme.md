# Homework 2 Part 1: Multinomial Naive Bayes
This homework assignent implements and tests a the multinomial naive bayes algorithm for text classification.

## How to run the code
The file associated with this readme is hw2_group3_part1.py

This code can be run as a python script. After running the file, the algorithm can be called as such:

```python
>>> getAccuracy('dataset 1', 'train')     
```
```python
>>> getAccuracy('dataset 1', 'test')   
```
The first parameter is the name of the directory that holds the training/test files. The second parameter describes the set of files to test the data on. If `train` is entered, the algorithm will use the training files to formulate its model, and also to test itself. If `test` is entered, the algorithm will use the training files to formulate its model and test it on the test files.

## Functions within the code 

`getFiles(path)`

    Input: string (path to directory containing files)
    Output: List of strings (containing paths to each file)

    This function takes a path to a directory and returns a list containing the path to each file in the directory.
    
    Calls: None
    Called by: getData

`getData(directory, filePurpose)`

    Input: string (name of directory containing training files, aka 'dataset 1/'), string ('train' or 'test')
    Output: dictionary {'ham' : hamTrainingFiles, 'spam' : spamTrainingFiles }

    This function takes in a directory and file purpose returns a dictionary containing the files in a data set for both classifications.
    
    Calls: getFiles
    Called by: getAccuracy

`getTokens(file)`
    
    Input: String (path to a file)
    Output: List of strings (terms)

    This function takes a file and returns a list of each token in the file.
        - All punctuation and numbers are removed.
        - All stop words are removed.
        - All terms are converted to lower case.
        - All terms are converted to their root form.
    
    Calls: None
    Called by: getTermCounts

`getTermGivenClass(term, setTerms)`

    Inputs: string (term), dictionary {term : count}
    Output: float ( P[term|class] )

    This function takes in a term and a dictionary of all terms and divides the number of occurrences of term by the total number of occurrences in the dictionary.
    
    Calls: None
    Called by: getClassGivenTerms

`getClassGivenTerms(terms, setTerms, pClass)`
    
    Inputs: string (terms), dictionary {term : count}, float (probability of an instance being of this class)
    Output: float (   log10( P[class|terms] )   )

    This function takes in all of the relevant terms in a file and a dictionary of all terms in a class and returns the logarithm of the probability that the file is classified as such given the file text.
    
    Calls: getTermGivenClass
    Called by: getClass

`getTermCounts(classes)`

    Input: dictionary {'ham' : hamTrainingFiles, 'spam' : spamTrainingFiles }
    Output: dictionary {'ham' : {term : count},    'spam' : {term : count} }

    This function returns a 2D dictionary. 
    The dictionary contains two sub-dictionaries.
    Each sub-dictionary contains every term in the classification and the number of times they occurred.
    
    Calls: getTokens
    Called by: getAccuracy

`getClass(file, classes, setTerms)`

    Input: string (path to file), dictionary {'ham' : {term : count},    'spam' : {term : count} }
    Output: string (classification)

    This function takes in a file and returns the most likely classification of the file.
    A 1 means the file is classified as spam.
    A 0 means the file is not classified as spam (and it thus classified as ham).
    
    Calls: getClassGivenTerms
    Called by: getAccuracy

`getAccuracy(dataSetDirectory, filePurpose)`

    Input: string (name of directory of the dataset), string ('test' or 'train')
    Output: None (prints the accurracy of the model)

    This function creates a model and tests it against another set of files. The accuracy of the model is printed.
    
    Calls: getData, getTermCounts, getClass
    Called by: None

## Results
Dataset 1:

    Training data: 99.34%
    Test data:     95.92%
    
Dataset 2:

    Training data: 100.00%
    Test data:     96.40%
    
Dataset 3:

    Training data: 100.00%
    Test data:     100.00%