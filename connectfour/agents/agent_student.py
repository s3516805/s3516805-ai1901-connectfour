from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random

class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]
        print (vals)
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        bestVal = 0
        
        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1))
            
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)
            
        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """ 
        return self._check_score(board)
    
    def _check_score(self, board):
        score = 0
        
        #Check center pieces
        center_piece = []
        for row in range(board.height):
            center_piece.append(board.get_cell_value(row,board.width//2))
        
        score += 3 * center_piece.count(self.id)
        
        #Check how many Horizontally
        for row in range(board.height):
            for col in range(board.width - 3):
                connect = [board.get_cell_value(row, col+i) for i in range(board.num_to_connect)]
                score += self._check_connect(connect) 
        
        #Check how many Vertically
        for col in range(board.width):
            for row in range(board.height - 3):
                connect = [board.get_cell_value(row+i, col) for i in range(board.num_to_connect)]
                score += self._check_connect(connect)
        
        #Check how many up diagonal
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                connect = [board.get_cell_value(row + 3 - i, col+i) for i in range(board.num_to_connect)]
                score += self._check_connect(connect)
              
        #Check how many down diagonal
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                connect = [board.get_cell_value(row+i, col+i) for i in range(board.num_to_connect)]
                score += self._check_connect(connect)
       
        return score
    
    def _check_connect(self,connect):
        score = 0
        
        if connect.count(self.id) == 4:
            score += 100
        elif connect.count(self.id) == 3 and connect.count(0) == 1:
            score += 5
        elif connect.count(self.id) == 2 and connect.count(0) == 2:
            score += 2
        elif connect.count(self.id%2+1) == 3 and connect.count(0) == 1:
            score -= 45

        return score