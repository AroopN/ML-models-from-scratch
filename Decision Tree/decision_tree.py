# decision_tree.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# personal and educational purposes provided that (1) you do not distribute
# or publish solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UT Dallas, including a link to http://cs.utdallas.edu.
#
# This file is part of Homework for CS6375: Machine Learning.
# Gautam Kunapuli (gautam.kunapuli@utdallas.edu)
# Sriraam Natarajan (sriraam.natarajan@utdallas.edu),
# Anjum Chida (anjum.chida@utdallas.edu)
#
#
# INSTRUCTIONS:
# ------------
# 1. This file contains a skeleton for implementing the ID3 algorithm for
# Decision Trees. Insert your code into the various functions that have the
# comment "INSERT YOUR CODE HERE".
#
# 2. Do NOT modify the classes or functions that have the comment "DO NOT
# MODIFY THIS FUNCTION".
#
# 3. Do not modify the function headers for ANY of the functions.
#
# 4. You may add any other helper functions you feel you may need to print,
# visualize, test, or save the data and results. However, you MAY NOT utilize
# the package scikit-learn OR ANY OTHER machine learning package in THIS file.

import numpy as np
import os
import graphviz


def contToDis(x):
    # x=list(x)
    # x=[int(i[:-1]) for i in x]
    # x=np.asarray(x)
    m = np.mean(x)
    new_attr = []
    for i in x:
        if i > m:
            new_attr.append(1)
        else:
            new_attr.append(0)
    return np.asarray(new_attr)


def partition(x):
    """
    Partition the column vector x into subsets indexed by its unique values (v1, ... vk)

    Returns a dictionary of the form
    { v1: indices of x == v1,
      v2: indices of x == v2,
      ...
      vk: indices of x == vk }, where [v1, ... vk] are all the unique values in the vector z.
    """
    

    # INSERT YOUR CODE HERE
    d = {}
    for i in range(len(x)):
        try:
            d[x[i]].append(i)
        except:
            d[x[i]] = [i]
    return d

    raise Exception('Function not yet implemented!')


def entropy(y):
    """
    Compute the entropy of a vector y by considering the counts of the unique values (v1, ... vk), in z

    Returns the entropy of z: H(z) = p(z=v1) log2(p(z=v1)) + ... + p(z=vk) log2(p(z=vk))
    """

    # INSERT YOUR CODE HERE
    from math import log2
    tot = len(y)
    d = partition(y)
    entropy = 0
    for i in d.keys():
      p = len(d[i])/tot
      entropy += -p * log2(p)
    return entropy

    raise Exception('Function not yet implemented!')


def mutual_information(x, y):
    """
    Compute the mutual information between a data column (x) and the labels (y). The data column is a single attribute
    over all the examples (n x 1). Mutual information is the difference between the entropy BEFORE the split set, and
    the weighted-average entropy of EACH possible split.

    Returns the mutual information: I(x, y) = H(y) - H(y | x)
    """

    # INSERT YOUR CODE HERE
    IG = entropy(y)
    d = partition(x)
    for i in d.values():
        a = []
        for j in i:
            a.append(y[j])
        IG -= len(i)/len(y)*entropy(a)
    return IG
    raise Exception('Function not yet implemented!')


def id3(x, y, attribute_value_pairs=None, depth=0, max_depth=5):
    """
    Implements the classical ID3 algorithm given training data (x), training labels (y) and an array of
    attribute-value pairs to consider. This is a recursive algorithm that depends on three termination conditions
        1. If the entire set of labels (y) is pure (all y = only 0 or only 1), then return that label
        2. If the set of attribute-value pairs is empty (there is nothing to split on), then return the most common
           value of y (majority label)
        3. If the max_depth is reached (pre-pruning bias), then return the most common value of y (majority label)
    Otherwise the algorithm selects the next best attribute-value pair using INFORMATION GAIN as the splitting criterion
    and partitions the data set based on the values of that attribute before the next recursive call to ID3.

    The tree we learn is a BINARY tree, which means that every node has only two branches. The splitting criterion has
    to be chosen from among all possible attribute-value pairs. That is, for a problem with two features/attributes x1
    (taking values a, b, c) and x2 (taking values d, e), the initial attribute value pair list is a list of all pairs of
    attributes with their corresponding values:
    [(x1, a),
     (x1, b),
     (x1, c),
     (x2, d),
     (x2, e)]
     If we select (x2, d) as the best attribute-value pair, then the new decision node becomes: [ (x2 == d)? ] and
     the attribute-value pair (x2, d) is removed from the list of attribute_value_pairs.

    The tree is stored as a nested dictionary, where each entry is of the form
                    (attribute_index, attribute_value, True/False): subtree
    * The (attribute_index, attribute_value) determines the splitting criterion of the current node. For example, (4, 2)
    indicates that we test if (x4 == 2) at the current node.
    * The subtree itself can be nested dictionary, or a single label (leaf node).
    * Leaf nodes are (majority) class labels

    Returns a decision tree represented as a nested dictionary, for example
    {(4, 1, False):
        {(0, 1, False):
            {(1, 1, False): 1,
             (1, 1, True): 0},
         (0, 1, True):
            {(1, 1, False): 0,
             (1, 1, True): 1}},
     (4, 1, True): 1}
    """

    # INSERT YOUR CODE HERE. NOTE: THIS IS A RECURSIVE FUNCTION.
    attribute_value_pairs = []
    for i in range(x.shape[1]):
        # print(i)
        col = list(x[:, i])
        col = partition(col)
        for j in col.keys():
            attribute_value_pairs.append((i, j))

    if len(set(y)) == 1:
      return y[0]
    elif len(attribute_value_pairs) == 0:
      return max(set(y), key=list(y).count)
    elif depth == max_depth:
      return max(set(y), key=list(y).count)

    mi = []
    for i in attribute_value_pairs:
        col = x[:, i[0]]
        x1 = []
        for j in col:
            if j == i[1]:
                x1.append(1)
            else:
                x1.append(0)
        mi.append(mutual_information(x1, list(y)))
    max_mi = -9999
    max_ind = -1

    for i in range(len(mi)):
        if mi[i] > max_mi:
            max_mi = mi[i]
            max_ind = i

    max_attr_pair = attribute_value_pairs[max_ind]
    true_index = np.where(x[:, max_attr_pair[0]] == max_attr_pair[1])[0]
    false_index = np.where(x[:, max_attr_pair[0]] != max_attr_pair[1])[0]

    new_x_t = np.delete(x, false_index, 0)
    # new_x_t = np.delete(new_x_t, max_attr_pair[0], 1)

    new_x_f = np.delete(x, true_index, 0)

    if len(set(new_x_f[:, max_attr_pair[0]])) == 1:
        new_x_f = np.delete(new_x_f, max_attr_pair[0], 1)

    new_y_t = np.delete(y, false_index, 0)
    new_y_f = np.delete(y, true_index, 0)
    attribute_value_pairs.remove(max_attr_pair)
    tree = {}
    if len(new_y_t) > 0:
        tree[(max_attr_pair[0], max_attr_pair[1], True)] = id3(
            new_x_t, new_y_t, attribute_value_pairs, depth+1, max_depth)
    if len(new_y_f) > 0:
        tree[(max_attr_pair[0], max_attr_pair[1], False)] = id3(
            new_x_f, new_y_f, attribute_value_pairs, depth+1, max_depth)
    # tree = {(max_attr_pair[0], max_attr_pair[1], True) = id3(new_x_t, new_y_t, attribute_value_pairs, depth+1, max_depth), (max_attr_pair[0], max_attr_pair[1], False) = id3(new_x_f, new_y_f, attribute_value_pairs, depth+1, max_depth)}
    return tree

    raise Exception('Function not yet implemented!')


def predict_example(x, tree):
    """
    Predicts the classification label for a single example x using tree by recursively descending the tree until
    a label/leaf node is reached.

    Returns the predicted label of x according to tree
    """

    # INSERT YOUR CODE HERE. NOTE: THIS IS A RECURSIVE FUNCTION.
    if not isinstance(tree, dict):
        return tree
    for i in tree.keys():
        if (x[i[0]] == i[1]) == i[2]:
            return predict_example(x, tree[i])

    raise Exception('Function not yet implemented!')


def compute_error(y_true, y_pred):
    """
    Computes the average error between the true labels (y_true) and the predicted labels (y_pred)

    Returns the error = (1/n) * sum(y_true != y_pred)
    """

    # INSERT YOUR CODE HERE
    c = 0
    n = len(y_true)
    for i in range(n):
        if y_true[i] != y_pred[i]:
            c += 1
    return c/n
    
    raise Exception('Function not yet implemented!')


def pretty_print(tree, depth=0):
    """
    Pretty prints the decision tree to the console. Use print(tree) to print the raw nested dictionary representation
    DO NOT MODIFY THIS FUNCTION!
    """
    if depth == 0:
        print('TREE')

    for index, split_criterion in enumerate(tree):
        sub_trees = tree[split_criterion]

        # Print the current node: split criterion
        print('|\t' * depth, end='')
        print('+-- [SPLIT: x{0} = {1} {2}]'.format(split_criterion[0], split_criterion[1], split_criterion[2]))

        # Print the children
        if type(sub_trees) is dict:
            pretty_print(sub_trees, depth + 1)
        else:
            print('|\t' * (depth + 1), end='')
            print('+-- [LABEL = {0}]'.format(sub_trees))


def render_dot_file(dot_string, save_file, image_format='png'):
    """
    Uses GraphViz to render a dot file. The dot file can be generated using
        * sklearn.tree.export_graphviz()' for decision trees produced by scikit-learn
        * to_graphviz() (function is in this file) for decision trees produced by  your code.
    DO NOT MODIFY THIS FUNCTION!
    """
    if type(dot_string).__name__ != 'str':
        raise TypeError('visualize() requires a string representation of a decision tree.\nUse tree.export_graphviz()'
                        'for decision trees produced by scikit-learn and to_graphviz() for decision trees produced by'
                        'your code.\n')

    # Set path to your GraphViz executable here
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    graph = graphviz.Source(dot_string)
    graph.format = image_format
    graph.render(save_file, view=True)


def to_graphviz(tree, dot_string='', uid=-1, depth=0):
    """
    Converts a tree to DOT format for use with visualize/GraphViz
    DO NOT MODIFY THIS FUNCTION!
    """

    uid += 1       # Running index of node ids across recursion
    node_id = uid  # Node id of this node

    if depth == 0:
        dot_string += 'digraph TREE {\n'

    for split_criterion in tree:
        sub_trees = tree[split_criterion]
        attribute_index = split_criterion[0]
        attribute_value = split_criterion[1]
        split_decision = split_criterion[2]

        if not split_decision:
            # Alphabetically, False comes first
            dot_string += '    node{0} [label="x{1} = {2}?"];\n'.format(node_id, attribute_index, attribute_value)

        if type(sub_trees) is dict:
            if not split_decision:
                dot_string, right_child, uid = to_graphviz(sub_trees, dot_string=dot_string, uid=uid, depth=depth + 1)
                dot_string += '    node{0} -> node{1} [label="False"];\n'.format(node_id, right_child)
            else:
                dot_string, left_child, uid = to_graphviz(sub_trees, dot_string=dot_string, uid=uid, depth=depth + 1)
                dot_string += '    node{0} -> node{1} [label="True"];\n'.format(node_id, left_child)

        else:
            uid += 1
            dot_string += '    node{0} [label="y = {1}"];\n'.format(uid, sub_trees)
            if not split_decision:
                dot_string += '    node{0} -> node{1} [label="False"];\n'.format(node_id, uid)
            else:
                dot_string += '    node{0} -> node{1} [label="True"];\n'.format(node_id, uid)

    if depth == 0:
        dot_string += '}\n'
        return dot_string
    else:
        return dot_string, node_id, uid


def train_IncomeData():
    # Load the training data
    import numpy as np
    import pandas as pd
    df = pd.read_csv("./Income.data",
                     header=None, delimiter=r"\s+",)
    df.columns = [
        "Age", "WorkClass", "fnlwgt", "Education", "EducationNum",
        "MaritalStatus", "Occupation", "Relationship", "Race", "Gender",
        "CapitalGain", "CapitalLoss", "HoursPerWeek", "NativeCountry", "Income"
    ]
    df = df.replace("?", None)
    df = df.dropna()
    df["Income"] = df["Income"].map({"<=50K": -1, ">50K": 1})
    y_all = df["Income"].values
    df.drop("Income", axis=1, inplace=True,)
    df.drop("CapitalGain", axis=1, inplace=True,)
    df.drop("CapitalLoss", axis=1, inplace=True,)
    df["HoursPerWeek"] = contToDis(df["HoursPerWeek"].to_numpy())
    df["Age"] = contToDis(df["Age"].to_numpy())
    df["EducationNum"] = contToDis(df["EducationNum"].to_numpy())
    df["fnlwgt"] = contToDis(df["fnlwgt"].to_numpy())


    df = df.to_numpy()
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        df, y_all, test_size=0.20, stratify=y_all, random_state=1100,
    )
    decision_tree = id3(X_train, y_train, max_depth=3)
    dot_str = to_graphviz(decision_tree)
    render_dot_file(dot_str, './IncomeData_tree')

    # # Compute the test error
    y_pred = [predict_example(x, decision_tree) for x in X_test]
    tst_err = compute_error(y_test, y_pred)
    from sklearn.metrics import confusion_matrix
    print(confusion_matrix(y_test, y_pred))

    print('Test Error = {0:4.2f}%.'.format(tst_err * 100))


if __name__ == '__main__':
    # Load the training data
    M = np.genfromtxt('./monks-1.train', missing_values=0, skip_header=0, delimiter=',', dtype=int)
    ytrn = M[:, 0]
    Xtrn = M[:, 1:]

    # Load the test data
    M = np.genfromtxt('./monks-1.test', missing_values=0, skip_header=0, delimiter=',', dtype=int)
    ytst = M[:, 0]
    Xtst = M[:, 1:]

    # Learn a decision tree of depth 3
    decision_tree = id3(Xtrn, ytrn, max_depth=3)

    # Pretty print it to console
    pretty_print(decision_tree)

    # Visualize the tree and save it as a PNG image
    dot_str = to_graphviz(decision_tree)
    render_dot_file(dot_str, './my_learned_tree')

    # Compute the test error
    y_pred = [predict_example(x, decision_tree) for x in Xtst]
    tst_err = compute_error(ytst, y_pred)

    print('Test Error = {0:4.2f}%.'.format(tst_err * 100))
    ###
    ###  OWN DATA
    ###

    print("TRAINING WITH Income.data")

    train_IncomeData()
