from util import entropy, information_gain, partition_classes
import numpy as np 
import ast
from collections import Counter
import time

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        #self.tree = {}
        pass

    def get_split_attr_val(self, dataX, dataY):
        '''
        Summary: Loop over all unique values in dataX and find the split
                 attribute and value which give the maximum information gain
        dataX: Numpy array of dimension (m,n)
        dataY: Numpy array of dimension (m,)
        '''
        num_row, num_col = dataX.shape
        IG_max, split_attr, split_val = 0, 0, dataX[0,0]
        for col_idx in range(num_col):
            attr_col = dataX[:,col_idx]
            for val in set(attr_col):
                y_left, y_right = partition_classes(dataX, dataY, col_idx, val)[2:4]
                temp_IG = information_gain(dataY, [y_left, y_right])
                if temp_IG > IG_max:
                    IG_max = temp_IG
                    split_attr, split_val = col_idx, val
        return split_attr, split_val

    def learn2(self, dataX, dataY):
        '''
        Summary: Build decision tree which is represented by a 2D array
        dataX: Numpy array of dimension (m,n)
        dataY: Numpy array of dimension (m,)
        '''
        if dataX.shape[0] == 1 or np.all(dataY == dataY[0]):
            return np.array([['leaf', dataY[0], None, None]], dtype=object)
        elif np.all(dataX == dataX[0,:]):
            y_count = Counter(dataY)
            return np.array([['leaf', max(y_count, key=lambda key: y_count[key]), None, None]], dtype=object)
        
        split_attr, split_val = self.get_split_attr_val(dataX, dataY)
        X_left, X_right, y_left, y_right = partition_classes(dataX, dataY, split_attr, split_val)

        if X_left.size == 0 or X_right.size == 0:
            y_count = Counter(dataY)
            return np.array([['leaf', max(y_count, key=lambda key: y_count[key]), None, None]], dtype=object)
        
        left_tree = self.learn2(X_left, y_left)
        right_tree = self.learn2(X_right, y_right)

        root = np.array([[split_attr, split_val, 1, left_tree.shape[0] + 1]], dtype=object)
        root = np.concatenate((root, left_tree), axis = 0)
        root = np.concatenate((root, right_tree), axis = 0)
        return root

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        '''
        X: A list of lists or numpy array of dimension (m,n)
        y: A list or numpy array of dimension (m,)
        '''
        X_arr = np.array(X, dtype=object)
        y_arr = np.array(y)
        self.tree = self.learn2(X_arr, y_arr)

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        '''
        Summary: Predict Y from the built decision tree for the given record
        record: A list of attributes
        '''
        def search(record, root):
            if root.shape[0] == 1:
                #assert(root[0][0] == 'leaf')
                return root[0][1]
            else:
                idx, rightNode_idx = int(root[0][0]), int(root[0][-1])
                attr = record[idx]
                if (isinstance(attr,  (int, float, long)) and attr <= root[0][1]) \
                    or (isinstance(attr,  str) and attr == root[0][1]):
                    return search(record, root[1:rightNode_idx])
                else:
                    return search(record, root[rightNode_idx:])

        Ypred = search(record, self.tree)
        return Ypred

if __name__=="__main__":
    #dataXY = np.array([[3, 'aa', 10, 1], [1, 'bb', 22, 1], [2, 'cc', 28, 0], \
    #                   [5, 'bb', 32, 0], [4, 'cc', 32, 0]], dtype=object)

    dataXY = np.genfromtxt('hw4-data.csv', delimiter=',', dtype=None, skip_header=1)
    dataXY = np.array([list(dataXY[i]) for i in range(dataXY.shape[0])], dtype=object)
    
    dataX = dataXY[:, :-1]
    dataY = dataXY[:, -1]

    start_time = time.time()
    DT = DecisionTree()
    DT.learn(dataX, dataY)
    
    Y_pred = []
    for record in dataX:
        Y_pred.append(DT.classify(record))

    results = [prediction == truth for prediction, truth in zip(Y_pred, dataY)]
    accuracy = float(results.count(True)) / float(len(results))

    print 'Elapsed Time: {:.4f}s'.format(time.time() - start_time)
    print 'Prediction Accuracy: {:.4f}'.format(accuracy)