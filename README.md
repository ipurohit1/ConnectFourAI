# Connect Four - CS5100 Capstone Project

This project uses two main algorithms: Minimax and Monte-Carlo Tree Search. 

## Minimax 
For minimax, a depth-limited search was implemented (to introduce a variable computer difficulty and to greatly reduce "thinking" time). This was done by developing a heuristic or evaluation function so that Minimax agent could explore the tree down to a specified depth and then evaluate these terminal states using a function. Additionally, minimax uses alpha-beta pruning in order to improve performance and avoid exploring branches that will not be factored into the maximizing/minimizing calculation.
Expectimax was also implemented to have an algorithm that plays well against suboptimal players. 

## MCTS
MCTS was our reinforcement learning approach to the Connect4 game, which offers a few distinct benefits. Firstly, MCTS is an asymmetric search, spending more time exploring promising branches. Secondly, MCTS does not require a heuristic and thus its performance is not dependent on how good its evaluation function is. 
