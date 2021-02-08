import constant as c
import math
import random
from utils import init_board, get_valid_column_moves, make_action, has_game_ended, opposite_player

class Node: 

    def __init__(self, board, parent=None): 
        self.board = board
        self.parent = parent
        self.visits = 0
        self.wins = 0 
        self.expected_value = 0
        self.children = {} # children nodes map to the action taken to get to the child node from current node 

    def calc_ucb(self): 
        # if self.visits == 0: 
        #     return c.INF
        if self.visits == 0: 
            return c.INF
        ucb = (self.wins/self.visits) + 2 * math.sqrt(2 * math.log(self.parent.visits)/ self.visits)
        return ucb 

    def max_child(self): 
        max_so_far = c.NINF
        max_child = None 

        for child in self.children:
            child_score = child.calc_ucb() 
            if child_score > max_so_far: 
                max_so_far = child_score
                max_child = child

        return max_child

    def max_child_win_ratio(self): 
        max_so_far = c.NINF
        max_child = None 

        for child in self.children:
            child_score = child.wins/child.visits
            if child_score > max_so_far: 
                max_so_far = child_score
                max_child = child

        return max_child



class MonteCarloTree:

    def __init__(self, tree = {}, root = None):
        self.tree = tree # dictionary that maps from state to node 
        self.root = root

    def print_tree(self): 
        for key in self.tree: 
            print(key, ' : ', self.tree[key])


def rollout(node, player):
    # keep track of starting_player and the starting board
    starting_player = player
    print('called rollout')
    state = node.board

    # keep picking random actions from current node until terminal node is reached 
    while True: 
        #print('rollout iterations')
        is_end, winner = has_game_ended(state)

        if is_end:
            if winner == starting_player:
                return winner, c.INF
            elif winner == opposite_player(starting_player):
                return winner, c.NINF
            else:
                return None, 0

        #print('passed if statemetns')
        valid_actions = get_valid_column_moves(state)
       # print('passed get valid column moves')
        random.shuffle(valid_actions)
       # print('passed shuffle')
        random_action = valid_actions[0]
       # print('passed retireval')
        state = make_action(state, player, random_action)
       # print('final pass')
        player = opposite_player(player)
        

def run_MCTS(player, board, MCT = None):

    # add the first node where the board is empty 
    # if MCT == None: 
    #     print('intitialize Node')
    #     #starting_state = init_board(6, 7)
    #     node = Node(board)
    #     # print('node.children ', node.children)
    #     # print('node type: ', type(node))
    #     current_tree = MonteCarloTree( {tuple(map(tuple, board)): node}, node)
    if MCT.root == None: 
        node = Node(board)
        MCT.root = node 
        current_tree = MCT
    else: 
        current_tree = MCT
        node = MCT.root
    

    while True: 
        # if the node is a leaf node and has no children 
        if len(node.children) != len(get_valid_column_moves(node.board)): 
            print('iteration')
            if node.visits == 0: 
                print('in node visits 0 branch')
                # add this node to the tree 
                current_tree.tree[ tuple (map(tuple, node.board))] = node 
                winner, value = rollout(node, player)
                print('winner', winner)
                break
            else: 
                print('in else branch where nodes will be added to tree')
                valid_moves = get_valid_column_moves(node.board)
                temp_node = None 
                for i in range(len(valid_moves)): 
                    # if i == 1: 
                    #     temp_node = Node(make_action(valid_moves[i], node))
                
                    new_state = make_action(node.board, player, valid_moves[i])
                    new_node = Node(new_state, node)
                    node.children[new_node] = valid_moves[i]
                    current_tree.tree[ tuple(map(tuple, new_state)) ] = new_node
                    if i == 1: 
                        temp_node = new_node


                node = temp_node
                winner, value = rollout(node, player)
                break 

        # node has all children, so find child with max UCB1 value 
        else: 
            max_child = node.max_child()
            node = max_child

    
    # backtrack 
    parent = node
    while node is not None: 
        node.visits += 1
        if player == winner: 
            node.wins += 1
        
        node = node.parent

    return current_tree
                
                


