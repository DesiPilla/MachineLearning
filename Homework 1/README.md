# Homework 1: Decision Tree Algorithm
This homework assignent implements and tests a decision tree algorithm. The two methods of creating the tree are:
* Information Gain Heuristic
* Variance Impurity Heuristic

## How to run the code
This code can be run from the command line using the following format:

```console
$ python hw1_group3_partN.py <L> <K> <training-set-path> <validation-set-path> <test-set-path> <to-print>
```
(part1 corresponds to the gain heuristic, part2 corresponds to the variance impurity heuristic)

Note: the arguments `training-set-path`, `validation-set-path`, and `test-set-path` must contain the full path to the csv files.
Below is an example of how to call the function:

```console
$ python hw1_group3_part1.py 3 3 "./data_sets1/training_set.csv" "./data_sets1/validation_set.csv" "./data_sets1/test_set.csv" True
$ python hw1_group3_part2.py 3 3 "./data_sets1/training_set.csv" "./data_sets1/validation_set.csv" "./data_sets1/test_set.csv" True
```

The three paths will be read into a pandas dataframe, and the code will begin to construct the tree. Once the decision tree is complete
(based on the training data), the 

`VI()`
This function takes in a data set as an input and returns the variance impurity heuristic.

`p()`
Inputs: data (dataframe), key (column name in the dataframe), binary value
Outputs: The probability of a the binary value being in the column of the dataframe.

`findEntropy()`
This function takes in a data set as an input and returns the entropy of a certain attribute.

`findGain()`
This function takes in a data set and an attribute as inputs and returns the information gain of the data, if it were to be split up by that attribute 

`findNode()`
This function takes in a data set and finds the best attribute by which to split that data set.
The attribute (Node) and information gain are returned.

`findChildren()`
This function takes a data set and a parent node as inputs.
The function determines which two attributes yield the highest information gain for (0, 1) values of the parent node, and assign them as children of the parent node.
The function calls itself recursively to find the children of its children, and continues until every chlid is a leaf.
The function does not return anything.

`buildTree()`
This function takes in a dataset and returns nothing.
The root node is found, and passed in as a parameter for the findChildren function, which builds the rest of the tree.

`def findNonleafNodes(A,B,C)`
This function returns a list with the nodes of a tree that are not leaves.

`printTree()`
This funciton prints the decision tree.

`findAccuracy()`
This function takes the test data as an input and returns the accuracy of the decision tree.

`findsubtree()`
This function takes a tree and finds the subtree needs to be substituted. 


`PostPruning()`
This function prunes the decision tree and returns the best tree.

`main()`
This runs the the code
