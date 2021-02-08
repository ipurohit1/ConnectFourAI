import click
from random import shuffle

from utils import handle_win, has_game_ended, init_board, make_action, make_minimax_move, minimax_2, print_board, expectimax, get_valid_column_moves
from spot import SPOT
import MCTS


class ConnectFourGame:
    def __init__(self, rows=6, columns=7, human_player=SPOT.RED):
        self.board = init_board(rows, columns, null_value=SPOT.EMPTY)
        if human_player == SPOT.RED:
            self.ai_player = SPOT.YELLOW
            self.human_player = SPOT.RED
        else:
            self.ai_player = SPOT.RED
            self.human_player = SPOT.YELLOW

    def play_game(self, game_type):
        print('Starting Board...\n')
        print_board(self.board)

        if game_type == '0player':
            self.both_ai_game()
        else:
            game_ended, winner = has_game_ended(self.board)
            i = 1
            
            #initialize MCT object 
            if game_type =='1player-MCTS':
                MCT = MCTS.MonteCarloTree()
                
            while not game_ended:
                try:
                    print('Move {}'.format(i))
                    i += (1 if game_type == '2player' else 2)

                    user_input = input('Enter a column number from 0 to {} or enter q to quit.\n'
                                       .format(len(self.board[0]) - 1))

                    if user_input == 'q':
                        print('User quit game.\n')
                        return

                    human_player = i % 2 != 0
                    column_number = int(user_input)
                    self.board = make_action(self.board,
                                             self.human_player if human_player else self.ai_player,
                                             column_number)
                    print_board(self.board)
                    game_ended, winner = has_game_ended(self.board)
                    if game_ended:
                        handle_win(winner)
                        return

                    if game_type == '1player-minimax' and not game_ended:
                        print('AI Move:\n')
                        
                        best_move, _ = make_minimax_move(self.board, self.ai_player, 5)
                        self.board = make_action(self.board, self.ai_player, best_move)
                        print_board(self.board)

                    if game_type == '1player-expectimax' and not game_ended: 
                        print('AI Move:\n')
                        
                        #best_move, _ = make_minimax_move(self.board, self.ai_player, 5)
                        best_move, _ = expectimax(self.board, self.ai_player, 5)
                        self.board = make_action(self.board, self.ai_player, best_move)
                        print_board(self.board)

                    if game_type == '1player-MCTS' and not game_ended:
                        n = 0
                       # MCT = MCTS.MonteCarloTree() #initialize tree object, with empty dictionary and root node

                        # print('tree type at the beginning: ', type(MCT.tree) )
                        # print('node type at the beginning: ', type(MCT.root) )
                        print('Running iterations of MCTS')
                        while n < 1000:
                            MCT = MCTS.run_MCTS(self.ai_player, self.board,  MCT) # doesn't specify MCT, so this MCT is created: MonteCarloTree( {tuple(map(tuple, starting_state)): node}, node)
                            n += 1
                        print('Finished running 100 iterations of MCTS')

                        print('AI Move:\n')
                        
                        board_to_tuple = tuple(map(tuple, self.board))
                       
                       # if the board is in the tree 
                        # print('tree: ', list(MCT.tree.keys())[0] )
                        # MCT.print_tree()
                        #print tree 
                        print('MCT Tree after iterations: ')
                        # for key in MCT.tree: 
                        #     print(key, ' : ', MCT.tree[key])

                        if board_to_tuple in MCT.tree:
                            node = MCT.tree[board_to_tuple]
                            max_child = node.max_child_win_ratio()
                            best_move = node.children[max_child] # returns move taken to get to child
                        else: 
                            print('random move')
                            moves = get_valid_column_moves(self.board)
                            shuffle(moves)
                            best_move = moves[0]

                        self.board = make_action(self.board, self.ai_player, best_move)
                        print_board(self.board) 
                        

                except IndexError as e:
                    print('ERROR:{}'.format(e))
                    print('Here is the current board for reference: \n')
                    print_board(self.board)
                    i = i - (1 if game_type == '2player' else 2)

                except ValueError:
                    print('ERROR: Not a valid number.')
                    print('Here is the current board for reference: \n')
                    print_board(self.board)
                    i = i - (1 if game_type == '2player' else 2)

                game_ended, winner = has_game_ended(self.board)

            handle_win(winner)
            return

    def both_ai_game(self):
        game_ended, winner = has_game_ended(self.board)
        i = 1
        players = [self.ai_player, self.human_player]
        depths = [3, 5]
        while not game_ended:
            print('Move {}'.format(i))
            print('{} Move:\n'.format(players[i % 2]))
            best_move, _ = minimax_2(self.board, players[i % 2], depths[i % 2])
            self.board = make_action(self.board, players[i % 2], best_move)
            print_board(self.board)
            i += 1
            game_ended, winner = has_game_ended(self.board)
        handle_win(winner)


@click.command()
@click.option('--rows', default=6, show_default=True,
              help='Specify the number of rows for the board.')
@click.option('--columns', default=7, show_default=True,
              help='Specify the number of columns for the board.')
@click.option('--game-type', default='2player', show_default=True,
              help='Specify the type of game to be played (2player represents two human players, '
                   'while 1player represents playing against an agent).')
def start_game(rows, columns, game_type):
    game = ConnectFourGame(rows=rows, columns=columns)
    game.play_game(game_type)


if __name__ == '__main__':
    start_game()
