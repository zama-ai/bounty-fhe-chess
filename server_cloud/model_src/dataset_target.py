import chess
import numpy as np
from torch.utils.data import Dataset
from helper_chessset import Board_State, Move_State


# # ⒹⒶⓉⒶⓈⒺⓉ 🅓🅐🅣🅐🅢🅔🅣 ⒹⒶⓉⒶⓈⒺⓉ    

helper_board_state = Board_State() 
helper_move_state = Move_State() 


class Chessset(Dataset):
    
    def __init__(self, games_df, size_data_set):
        """which raw data"""
        super(Chessset, self).__init__()
        self.size_data_set = size_data_set
        self.games_df = games_df


    def __len__(self):
        """returns the dataset's size"""
        return self.size_data_set


    def __getitem__(self, idx):

        # get the game
        random_game = self.games_df.values[idx]
        initial_moves = helper_move_state.list_move_sequence(random_game)

        # get random move
        game_state_i = np.random.randint(len(initial_moves)-1)
        next_move = initial_moves[game_state_i]  # piece_pos

        # get the sequence of moves until the move
        moves = initial_moves[:game_state_i]

        # instantiate board from chess lib
        board = chess.Board()

        for move in moves:
            board.push_san(move)

        chessboard = helper_board_state.board_tensor_12(board)          # shape(6,8,8) or shape(12,8,8)
        
        source,target = helper_move_state.from_to_bitboards(next_move, board) # shape (1)

        # determine white or black turn (1 for w, -1 for b) and then the one to play has always positive value
        if game_state_i %2 == 1:
            chessboard *= -1
        return chessboard,source,target
