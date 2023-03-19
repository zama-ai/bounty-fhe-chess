import numpy as np
from peewee import SqliteDatabase

# pawn_table = np.array([
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [98, 134, 61, 95, 68, 126, 34, -11],
#     [-6, 7, 26, 31, 65, 56, 25, -20],
#     [-14, 13, 6, 21, 23, 12, 17, -23],
#     [-27, -2, -5, 12, 17, 6, 10, -25],
#     [-26, -4, -4, -10, 3, 3, 33, -12],
#     [-35, -1, -20, -23, -15, 24, 38, -22],
#     [0, 0, 0, 0, 0, 0, 0, 0]
# ])

# tops = np.argpartition(pawn_table, kth=1, axis=1)
# #topuno = tops[tops]
# print(tops)

db = SqliteDatabase("/Volumes/vrona_SSD/lichess_data/wb_2000_database.db")

db.connect()
