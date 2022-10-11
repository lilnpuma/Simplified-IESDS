"""
I pledge on my honor that I have not given or received
any unauthorized assistance on this project.
Manu Madhu Pillai
"""
import sys
import copy as cp
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


def cataloger(g_mat, action):
    """
    Returns integer index for a given string action.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.
                    action (string): action.
            Returns:
                    int: index of the action.
    """
    for i in range(len(g_mat[0])):
        for j in range(len(g_mat[0][i])):
            if action is g_mat[0][i][j]:
                return 10*i + j  # Storing action indexing in a 2 digit integer index variable
    return -1

def get_payoff(g_mat, player, action):
    """
    Returns payoff values for a given player in a given action from the payoff matrix.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.
                    player (int): Player ID.
                    action (string): action.
            Returns:
                    array: Returns a numpy nd array containing payoff values.
    """
    loc = cataloger(g_mat, action)
    if loc // 10 == 0:
        return g_mat[1][loc % 10, :, :, player]
    if loc // 10 == 1:
        return g_mat[1][:, loc % 10, :, player]
    if loc // 10 == 2:
        return g_mat[1][:, :, loc % 10, player]
    return -1


def dominates1(g_mat, player, action_1, action_2):
    """
    Returns True if a strictly dominates b, and False otherwise.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.
                    player (int): Player ID.
                    action_1 (string): Pressumed dominant action.
                    action_2 (string): Pressumed non-dominant action.
            Returns:
                    bool: The return value. True for success, False otherwise.
    """
    payoffa = get_payoff(g_mat, player, action_1)
    payoffb = get_payoff(g_mat, player, action_2)
    # check flag to verify if payoff of action a is greater in atleast one instance.
    dom_check = 0
    for i in range(payoffa.shape[0]):
        for j in range(payoffa.shape[1]):
            if payoffa[i][j] < payoffb[i][j]:
                return False
                # checking if payoff of action a is lesser than action b in any instance.
            if payoffa[i][j] > payoffb[i][j]:
                dom_check = 1
                # checking if payoff of action a is greater than action b in atleast one instance.
    if dom_check != 0:
        return True
        # payoff of a is greater than payoff of action b in atleast one instance,
        # and equal in other instances.
    return False
        # payoff of a is equal to payoff of action b in all instances.


def dominated1(g_mat):
    """
    Returns the strictly dominant actions in the game.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.

            Returns:
                    list: Returns the strictly dominant actions in the game as a list of tuples.

    """
    possible_args = []  # possible action pairs to check for dominant actions
    dominated_pairs = []

    for i in range(len(g_mat[0])):
        for j in range(len(g_mat[0][i])):
            for k in range(len(g_mat[0][i])):
                if j != k:
                    possible_args.append((i, g_mat[0][i][j], g_mat[0][i][k]))

    for action in possible_args:
        # check if action 1 is strictly dominates action 2.
        if dominates1(g_mat, action[0], action[1], action[2]) is True:

            dominated_pairs.append((action[0], action[2], action[1]))

    for i in range(len(dominated_pairs)-1):
        if dominated_pairs[i][0] == dominated_pairs[i+1][0]:
            # removes multiple entries in a particular player's dominant action set.
            dominated_pairs.pop()

    return dominated_pairs


def reduce(g_mat, player, action):
    """
    Returns Tuple containing reduced action set and reduced payoff matrix.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.
                    player (int): Player ID.
                    action (string): Action to be reduced.
            Returns:
                    tuple: Reduced action set and reduced payoff matrix.
    """

    action_temp = cp.deepcopy(g_mat[0])
    loc = cataloger(g_mat, action)
    if loc // 10 is not player:  # checking if action corresponds to the player
        print("Error, player doesnt correspond to action.")
        return -1
    action_temp[loc // 10].pop(loc % 10)
    # removes the particular action set
    return ((action_temp, np.delete(g_mat[1], [loc % 10], axis=player)))


def iesds1(g_mat):
    """
    Returns Tuple containing reduced action set and reduced payoff matrix
    based on a simplified version of Iterated Elimination of Strictly
    Dominated Strategies (IESDS).

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.
            Returns:
                    tuple: Reduced action set and reduced payoff matrix.
    """
    dominated_pairs = dominated1(g_mat)
    g_temp = cp.deepcopy(g_mat)
    for i in dominated_pairs:
        # sequentially remove dominated action sets to obtain reduced matrix based on IESDS.
        g_temp = reduce(g_temp, i[0], i[1])
    return (dominated_pairs, g_temp)


def dominated2(g_mat):
    """
    Returns the strictly dominant actions in the game including mixed strategies.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.

            Returns:
                    list: Returns the strictly dominant actions in the game as a list of tuples.

    """
    return 0


def eisds2(g_mat):
    """
    Returns Tuple containing reduced action set and reduced payoff matrix
    based on Iterated Elimination of Strictly Dominated Strategies (IESDS).
    Includes mixed strategies.

            Parameters:
                    g_mat (tuple): Tuple containing action set and payoff matrix.
            Returns:
                    tuple: Reduced action set and reduced payoff matrix.
    """
    return 0


def main():
    """
    Contains test cases for the functions defined above.
        Parameters:
                nil
        Returns:
                int: infers function has run succesfully.
    """
    #Tests for dominates1
    print(dominates1(g1, 0, 'a0', 'a0'))
    print(dominates1(g1, 0, 'a0', 'a1'))
    print(dominates1(g1, 0, 'a1', 'a0'))
    print(dominates1(g1, 2, 'c0', 'c1'))
    print(dominates1(g1, 2, 'c1', 'c2'))

    #Tests for dominated1
    print(dominated1(g1))

    # Tests for reduce
    print(reduce(g1, 2, 'c2'))
    g_new = reduce(g1, 2, 'c2')
    print(reduce(g_new, 0, 'a0'))

    # Tests for iesds1
    print(iesds1(g1))

    return 0


if __name__ == '__main__':
    sys.exit(main())
