"""
I pledge on my honor that I have not given or received
any unauthorized assistance on this project.
Manu Madhu Pillai
"""

import numpy as np

m00 = np.array([[1, 3, 1], [2, 0, 1], [3, 0, 0]])
m01 = np.array([[2, 1, 1], [1, 1, 1], [2, 5, 0]])
m02 = np.array([[1, 0, 1], [2, 4, 1], [3, 0, 0]])
m0 = np.array([m00, m01, m02])
m10 = np.array([[0, 3, 1], [1, 0, 1], [2, 0, 0]])
m11 = np.array([[1, 1, 1], [0, 1, 1], [1, 5, 0]])
m12 = np.array([[0, 0, 1], [1, 4, 1], [2, 0, 0]])
m1 = np.array([m10, m11, m12])
m = np.array([m0, m1])

actions = [["a0", "a1"], ["b0", "b1", "b2"], ["c0", "c1", "c2"]]
g1 = (actions, m)


def cataloger(a):
    """
    Returns integer index for a given string action.

            Parameters:
                    a (string): action
            Returns:
                    int: index of the action.
    """
    loc = 0

    if "b" in a:
        loc += 10
    elif "c" in a:
        loc += 20

    if "1" in a:
        loc += 1
    elif "2" in a:
        loc += 2
    
    return loc


def getPayoff(g, i, a):
    """
    Returns payoff values for a given player in a given action from the payoff matrix.

            Parameters:
                    g (tuple): Tuple containing action set and payoff matrix.
                    i (int): Player ID.
                    a (string): action
            Returns:
                    array: Returns a numpy nd array containing payoff values.
    """
    loc = cataloger(a)
    if loc // 10 == 0:
        return g[1][loc % 10, :, :, i]
    if loc // 10 == 1:
        return g[1][:, loc % 10, :, i]
    if loc // 10 == 2:
        return g[1][:, :, loc % 10, i]

def dominates1(g, i, a, b):
    """
    Returns True if a strictly dominates b, and False otherwise.

            Parameters:
                    g (tuple): Tuple containing action set and payoff matrix.
                    i (int): Player ID.
                    a (string): Pressumed dominant action.
                    b (string): Pressumed non-dominant action.
            Returns:
                    bool: The return value. True for success, False otherwise.
    """
    payoffa = getPayoff(g, i, a)
    payoffb = getPayoff(g, i, b)
    dom_check = 0
    for i in range(payoffa.shape[0]):
        for j in range(payoffa.shape[1]):
            if payoffa[i][j] < payoffb[i][j]:
                return False
            if payoffa[i][j] > payoffb[i][j]:
                dom_check = 1
    if dom_check != 0:        
        return True
    else:
        return False


def dominated1(g):
    return 0


def reduce(g, i, a):
    return 0


def iesds(g):
    return 0


def dominated2(g):
    return 0


def eisds2(g):
    return 0

""" Tests for dominates1 """
# print(dominates1(g1, 0, 'a0', 'a0'))
# print(dominates1(g1, 0, 'a0', 'a1'))
# print(dominates1(g1, 0, 'a1', 'a0'))
# print(dominates1(g1, 2, 'c0', 'c1'))
# print(dominates1(g1, 2, 'c1', 'c2'))