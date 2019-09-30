# Homework 1 Group Project 
# ********************* Implement tree using variance impurity heuristic ******************************
import pandas as pd
import sys
import math
import random

#data1 = pd.read_csv('./data_sets1/training_set.csv')
#data2 = pd.read_csv('./data_sets2/training_set.csv')
#test_data1 = pd.read_csv('./data_sets1/test_set.csv')
#test_data2 = pd.read_csv('./data_sets2/test_set.csv')
#validation_data1 = pd.read_csv('./data_sets1/validation_set.csv')
#validation_data2 = pd.read_csv('./data_sets2/validation_set.csv')

counter = 0

class Node():
    ''' This is a class to store all node information '''
    def __init__(self, name, gain, parent=None, children=[None, None], isLeaf=False, leafVal=999):
        self.name = name            # Name of attribute; i.e. 'XM'
        self.gain = gain
        self.parent = parent        # Instance of parent node
        self.children = children    # Instance of children nodes: [child0, child1]
        self.leafVal = leafVal      # If the node is not a leaf, leafVal = 999. If the node is a leaf, leafVal = 0 or 1
            
    def __repr__(self):
#        return'Node: %s  \tParent: %s \tChildren: %s %s \tClassification: %d' % (self.name, self.parent.name, self.parent.children[0].name, self.parent.children[1].name,self.leafVal)
        return'Node: %s \tGain: %.6f \tParent: %s \tClassification: %d' % (self.name, self.gain, self.parent.name, self.leafVal)
       

def VI(data):
    ''' Get the variance impurity heuristic of the data. '''
    k = len(data['Class'])
    k0 = sum(data['Class'] == 0)
    k1 = sum(data['Class'] == 1)
    return (k0/k)*(k1/k)

def p(data, key, val):
    ''' Get the probability of a certain value being in a certain column of the data. '''
    return data[data[key] == val][key].size / data[key].size

def findEntropy(data):
    ''' Get the Entropy of a certain attribute. '''

    n = float(len(data['Class']))
    n0 = float(sum(data['Class'] == 0))
    n1 = float(sum(data['Class'] == 1))
    #print(n)
    try:
        if n0==0:
            return -n1/n*math.log(n1/n,2)
        elif n1==0:
            return -n0/n*math.log(n0/n,2)    
        else:
            return -n1/n*math.log(n1/n,2)-n0/n*math.log(n0/n,2)
    except:
        pass


def findGain(data, key):
    ''' Find the gain of the data for splitting it by a certain attribute. '''

    vi = VI(data)
    for val in [0, 1]:
        try:
            pr = p(data, key, val)
            vix = VI(data[data[key] == val])
            vi -= pr*vix
        except:             # If data is pure, it will throw a divide by zero error 
            pass
    return vi
 

def findNode(data):
    ''' Find the best attribute by which to split a data set. '''
    node = 'LEAF'                   # Assume the node is a leaf
    maxGain = 0
    for key in data.keys()[:-1]:
        gain = findGain(data, key)
        if gain > maxGain:
            node = key              # If the node is not a leaf, name it properly
            maxGain = gain
    return node, maxGain
  
    

def findChildren(data, parentNode):
    ''' This function is recursive, and will find each branch until it hits a leaf.
    When a leaf is found, it will return and continue to build the next branch.'''
    global counter
    if parentNode.gain == 0:
        return
    
    split0 = data[data[parentNode.name] == 0]
    split0 = split0.drop(columns=parentNode.name)
    name0, gain0 = findNode(split0)
    node0 = Node(name0, gain0, parentNode)
    
    if node0.name == 'LEAF':
        node0.leafVal = split0['Class'].values[0]
    
    split1 = data[data[parentNode.name] == 1]
    split1 = split1.drop(columns=parentNode.name)
    name1, gain1 = findNode(split1)
    node1 = Node(name1, gain1, parentNode)

    if node1.name == 'LEAF':
        node1.leafVal = split1['Class'].values[0] 
    
    treedict[parentNode.name,counter]={}
    if node0.name == 'LEAF':
        treedict[parentNode.name,counter][0] = node0.leafVal
    else:
        treedict[parentNode.name,counter][0] = node0.name
        
    if node1.name == 'LEAF' :
        treedict[parentNode.name,counter][1] = node1.leafVal
    else:
        treedict[parentNode.name,counter][1] = node1.name
        
    treelist.append(parentNode.name)
    counter += 1
    
    parentNode.children = [node0, node1]
    
    findChildren(split0, node0)
    findChildren(split1, node1)
    return


def buildTree(data):
    ''' This builds the entire decision tree for a dataset''' 
    rootAttr, gain = findNode(data)         # Find the root node first
    parentNode = Node(rootAttr, gain)       # Create a Node instance of the root node
    findChildren(data, parentNode)          # Pass in the root node and build the rest of the tree
    
def findNonleafNodes(A,B,C):
    for i in range(0,len(C)):
        if C[i]!=2 and B[i]==0:
            for j in range(i+1,len(C)):
                if A[j] == A[i]:
                    if C[j]!=2:
                        break
        else:
            nonleafnodes.append(i)
            
    NL = nonleafnodes.copy()
    return NL
    
def printTree(to_print):
    listintent = []
    listname = []
    listpos = []
    intent = 0
    pos = 0
    for i in range (0,counter):
        #If the node's children are both leaves
        if (treedict[treelist[i],i][0]==0 or treedict[treelist[i],i][0]==1) and (treedict[treelist[i],i][1]==0 or treedict[treelist[i],i][1]==1):
            if to_print == 'yes':
                print('|\t'*intent, treelist[i],'=0:', treedict[treelist[i],i][0])
                print('|\t'*intent, treelist[i],'=1:', treedict[treelist[i],i][1])
            queuelist.append(treelist[i])
            vallist.append(0)
            leaflist.append(treedict[treelist[i],i][0])
            queuelist.append(treelist[i])
            vallist.append(1)
            leaflist.append(treedict[treelist[i],i][1])
            intent = listintent[pos-1]
            times=1
            while(1):
                if (treedict[listname[-1],listpos[-1]][1]==0 or treedict[listname[-1],listpos[-1]][1]==1):
                    if to_print == 'yes':
                        print('|\t'*intent,listname[-1],'=1:',treedict[listname[-1],listpos[-1]][1])
                    queuelist.append(listname[-1])
                    vallist.append(1)
                    leaflist.append(treedict[listname[-1],listpos[-1]][1])
                    if i==counter-1:
                        try:
                            if to_print == 'yes':
                                print('|\t'*(intent-3),listname[-2],'=1:',treedict[listname[-2],listpos[-2]][1])
                            queuelist.append(listname[-2])
                            vallist.append(1)
                            leaflist.append(treedict[listname[-2],listpos[-2]][1])
                            try:
                                if to_print == 'yes':
                                    print('|\t'*(intent-5),listname[-3],'=1:',treedict[listname[-3],listpos[-3]][1])
                                queuelist.append(listname[-3])
                                vallist.append(1)
                                leaflist.append(treedict[listname[-3],listpos[-3]][1])
                                break
                            except:
                                #pass
                                break
                        except:
                            #pass
                            break

                        
                    intent = listintent[-1]
                    del(listintent[-1])
                    del(listname[-1])
                    del(listpos[-1])
                    pos -= 1
                    intent = listintent[-1]
                    times += 1
                else:
                    if to_print == 'yes':
                        print('|\t'*intent,listname[-1],'=1:')
                    queuelist.append(listname[-1])
                    vallist.append(1)
                    leaflist.append(2)
                    del(listintent[pos-1])
                    del(listname[pos-1])
                    del(listpos[pos-1])
                    pos -= 1
                    intent += 1
                    break
                
            
            continue
        #If the zero-child of the node is leaf
        if (treedict[treelist[i],i][0]==0 or treedict[treelist[i],i][0]==1):
            if to_print == 'yes':
                print('|\t'*intent, treelist[i]+ '=0:', treedict[treelist[i],i][0])
                print('|\t'*intent, treelist[i]+ '=1:')
            queuelist.append(treelist[i])
            vallist.append(0)
            leaflist.append(treedict[treelist[i],i][0])
            queuelist.append(treelist[i])
            vallist.append(1)
            leaflist.append(2)
            intent += 1
            continue
        #In all the other cases
        listname.append(treelist[i])
        listintent.append(intent)
        listpos.append(i)
        queuelist.append(treelist[i])
        vallist.append(0)
        leaflist.append(2)
        pos +=1
        if to_print == 'yes':
            print('|\t'*intent, treelist[i],'=0:')
        intent +=1
        
        
def findAccuracy(test_data,A,B,C):
    if type(test_data) == str:
        test_data = pd.read_csv(test_data)
    right_class = []
    wrong_class = []
    subtree_pointer = 0
    counter1=0
    flag = 0
    for row in range(0,len(test_data)):
        counter1 +=1
        flag = 0
        subtree_pointer = 0
        while(flag==0):
            
            for k in range(0,20):
                
                
                if test_data.keys()[k]==A[subtree_pointer]:
                    
                    if (test_data[test_data.keys()[k]][row] != B[subtree_pointer]):
                        
                        for j in range(subtree_pointer+1,len(A)):
                                if A[j] == A[subtree_pointer]:
                                    subtree_pointer = j
                                    break
                        break
                    else:    
                        
                        if C[subtree_pointer] !=2:
                            if (test_data['Class'][row] == C[subtree_pointer]):
                                right_class.append(1)
                                flag = 1
                                break
                            else:
                                wrong_class.append(1)
                                flag = 1
                                break
                        else:
                            if (test_data[test_data.keys()[k]],row == 0):
                                subtree_pointer += 1
                                break
    
    
    return(len(right_class)/len(test_data))
        
    
#------------------------- Still needs work -----------------------------------

def findsubtree(P,A,B,C):
    sum_ones = 0
    sum_zeros = 0
    subtree_root = A[P]
    if subtree_root == A[0]:      #If the random root of the subtree is the actual root
        for j in range(0,len(A)):
            if C[j] != 2:
                if C[j] == 0:
                    sum_zeros += 1
                else:
                    sum_ones += 1
        if sum_zeros >= sum_ones:
            leaf_value = 0
        else:
            leaf_value = 1
        start = 0
        end = len(A)
    else:                               #If not
        if B[P]==0:
            node = P
        else:
            e = P-1
            for i in range(e,0,-1):
                if A[i]==A[P]:
                    node = i
                    break
    
                
        if B[node-1]==0:
            start = node
            end = 0
            for s in range(node,len(A)):
                if A[s]==A[node-1]:
                    end = s
                    break
            for k in range (start,end):
                subtreename.append(A[k])
                subtreeval.append(B[k])
                subtreeleaf.append(C[k])
                if C[k]!=2:
                    if C[k]==0:
                        sum_zeros +=1
                    else:
                        sum_ones +=1
            if sum_zeros >= sum_ones:
                leaf_value = 0
            else:
                leaf_value = 1

        else:
            e = node-2
            name = A[node-1]

            flag=0
            while (flag==0):
                for i in range(e,0,-1):
                    if A[i]==name:     
                        if name==A[0]:
                            for k in range (node,len(A)):
                                subtreename.append(A[k])
                                subtreeval.append(B[k])
                                subtreeleaf.append(C[k])
                                if C[k]!=2:
                                    if C[k]==0:
                                        sum_zeros +=1
                                    else:
                                        sum_ones +=1
                            if sum_zeros >= sum_ones:
                                leaf_value = 0
                            else:
                                leaf_value = 1
                            flag = 1
                            start = node
                            end = len(A)
                        break
                        
                        if A[i-1]==A[0] and B[i-1]==1:
                            for k in range (node,len(A)):
                                subtreename.append(A[k])
                                subtreeval.append(B[k])
                                subtreeleaf.append(C[k])
                                if C[k]!=2:
                                    if C[k]==0:
                                        sum_zeros +=1
                                    else:
                                        sum_ones +=1
                            if sum_zeros >= sum_ones:
                                leaf_value = 0
                            else:
                                leaf_value = 1
                            flag = 1
                            start = node
                            end = len(A)
                        break
                            
                            
                        if C[i]!=2 and B[i-1]==1:
                            name = A[i-1]
                            e = i-2
                        break
                        
                        if C[i]!=2 and B[i-1]==0:
                            for s in range(i,len(A)):
                                if A[s]==A[i-1]:
                                    end = s
                                    break
                            for k in range (node,end):
                                subtreename.append(A[k])
                                subtreeval.append(B[k])
                                subtreeleaf.append(C[k])
                                if C[k]!=2:
                                    if C[k]==0:
                                        sum_zeros +=1
                                    else:
                                        sum_ones +=1
                            if sum_zeros >= sum_ones:
                                leaf_value = 0
                            else:
                                leaf_value = 1
                            start = node
                            flag=1
                        break
                        
                        if B[i-1]==0:
                            for s in range(i,len(A)):
                                if A[s]==A[i-1]:
                                    end = s
                                    break
                            for k in range (node,end):
                                subtreename.append(A[k])
                                subtreeval.append(B[k])
                                subtreeleaf.append(C[k])
                                if C[k]!=2:
                                    if C[k]==0:
                                        sum_zeros +=1
                                    else:
                                        sum_ones +=1
                            if sum_zeros >= sum_ones:
                                leaf_value = 0
                            else:
                                leaf_value = 1
                            start = node
                            flag = 1
                        break
                                
                        if B[i-1]==1:
                            name = A[i-1]
                            e = i-2
                        break
                    else:
                        continue
                leaf_value = 0
                start = P
                end = P+1
                flag = 1       
    return(leaf_value,start,end)
            
 # -----------------------------------------------------------------------------------       


def PostPruning(L,K,val_data,test_data):
    queuelist_best = queuelist.copy()
    vallist_best = vallist.copy()
    leaflist_best = leaflist.copy()
    queuelist_original = queuelist.copy()
    vallist_original = vallist.copy()
    leaflist_original = leaflist.copy() 
   
    
    for i in range (0,L):
        M = random.randrange(K)
        accuracy = findAccuracy(val_data,queuelist_best,vallist_best,leaflist_best)
        for j in range (0,M):
            NL = findNonleafNodes(queuelist_best,vallist_best,leaflist_best)
            P = random.randrange(len(NL))
            pos = NL[P]
            leaf,start,end = findsubtree(pos,queuelist_best,vallist_best,leaflist_best)
                
            leaflist[start-1] = leaf

            del queuelist[start:start+len(subtreeleaf)]
            del vallist[start:start+len(subtreeleaf)]
            del leaflist[start:start+len(subtreeleaf)]
            
        new_accuracy = findAccuracy(val_data,queuelist,vallist,leaflist)
        if (new_accuracy >= accuracy):
            queuelist_best = queuelist.copy()
            vallist_best = vallist.copy()
            leaflist_best = leaflist.copy()
    
    
    accuracy = findAccuracy(test_data,queuelist_original,vallist_original,leaflist_original)
    new_accuracy = findAccuracy(test_data,queuelist_best,vallist_best,leaflist_best)
    print('Accuracy of post-prunned tree = ',new_accuracy*100, '%')
            
                        
#    queuelist[start+1] = queuelist_original[start]
#    vallist[start+1] = 1
#    leaflist[start+1] = leaf
                        
#    print('original')
#    for k in range(start-2,start+15):#len(leaflist_original)):
#        print(queuelist_original[k],vallist_original[k],leaflist_original[k])
#    
#    
#    print('after')
#    for k in range(start-2,start + 10):#len(leaflist)):
#        
#        print(queuelist[k],vallist[k],leaflist[k])
                
    
treelist = []

queuelist = []
vallist = []
leaflist = []
queuelist_original = []
vallist_original = []
leaflist_original = []

queuelist_best = []
vallist_best = []
leaflist_best = []

subtreename = []
subtreeval = []
subtreeleaf = []
nonleafnodes = []

treedict = {} 

print('-------------- (Assignment 1 - Group 3) --------------')

#*sys.argv[L,K,trainingdata,testdata,validationdata,to_print]
L = int(sys.argv[1])
K = int(sys.argv[2])
trainingdata = sys.argv[3]
testdata = sys.argv[4]
validationdata = sys.argv[5]
to_print = sys.argv[6]

data = pd.read_csv(trainingdata)
test_data = pd.read_csv(testdata)
validation_data = pd.read_csv(validationdata)

buildTree(data)
printTree(to_print)
PostPruning(L,K,validationdata,testdata)

#buildTree(data2)
#printTree('no')
#accuracy = findAccuracy(test_data2,queuelist,vallist,leaflist)
#print('Accuracy of the tree = ', accuracy*100, '%')
#PostPruning(3,3,validation_data2,test_data2)



#accuracy = findAccurancy(test_data1)
#print('--------------------------------------------------------------')
#print('Accuracy = ', accuracy*100, '%')

#for j in range (0,len(queuelist)):
#    
#    print(queuelist[j],vallist[j],leaflist[j])
    

    
#print(treedict)


