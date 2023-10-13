import numpy as np

# screenplay dimension
sp_width = 800
sp_height = 800

"""
RECALL:
homemade chessboard row starts at 0 from top // col starts at 0 from left
python-chess library (https://python-chess.readthedocs.io): within chessboard, rows start at "1" from bottom  // cols start at "a" from left // bitboard from 0 to 63 squares (see below)
"""

# homemade chessboard (8*8)
cb_cols = 8                     #number of columns
cb_rows = 8                     #number of rows
sqsize = sp_width // cb_cols    #size of squares


"""
Python-Chess lib. uses alphanumeric coordinates (e2 equivalent to col 1 - row 2) but also
bitboard logic: an array of square table location within chessboard.
the move e2e4 becomes 8 to 24.
"""
bitboard = np.array([
    [56,57,58,59,60,61,62,63],
    [48,49,50,51,52,53,54,55],
    [40,41,42,43,44,45,46,47],
    [32,33,34,35,36,37,38,39],
    [24,25,26,27,28,29,30,31],
    [16,17,18,19,20,21,22,23],
    [8,9,10,11,12,13,14,15],
    [0,1,2,3,4,5,6,7],
    ])

"""
Hash tables:
- dict of square_alphanum (square: alphanumeric),
- dict of alphanum_square (alphanumeric: square).

col = ["a", "b", "c", "d", "e", "f", "g", "h"]
row = [1,2,3,4,5,6,7,8]
bitalpha = []
square_alphanum = {}

for ic in np.ndenumerate(bitboard):
    square_alphanum[ic[1]] = "%s%s" %(col[ic[0][1]],row[7-ic[0][0]])

alphanum_square = {v: k for k, v in square_alphanum.items()}
"""
alphanum_square = {'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63,
                   'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
                   'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
                   'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
                   'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
                   'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
                   'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
                   'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7,}