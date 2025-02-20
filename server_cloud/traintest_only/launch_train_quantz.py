import sys
import torch.nn as nn
from torch.utils.data import DataLoader

import numpy as np
import pandas as pd

"""
Training Only here
Recall for TESTING, please run launch_(test)_compile_fhe.py
"""

#source
from train_source_quantz import train_valid

sys.path.append("model_src/")
from dataset_source import Chessset

# target
#from train_target_quantz import train_valid
#from dataset_target import Chessset

sys.path.append("model_src/quantz/")
# source
from source_44cnn_quantz import QTChessNET

# target (for training only) 
#from target_44cnn_quantz import QTtrgChessNET # CAUTION "target_44cnn_quantz_EVAL" is for Inference

"""
LOADING SECTION
training_set = Chessset(dataset['AN'])
"""

# 🅢🅟🅛🅘🅣 🅓🅐🅣🅐

game_move_set = "data/wb_2000_300.csv"
wechess = pd.read_csv(game_move_set)

# split dataset splitted into: training_set (80%), valid_set (20%), test_set (20%)
training_set, valid_set, test_set = np.split(wechess.sample(frac=1, random_state=42), [int(.6*len(wechess)), int(.8*len(wechess))])


# 🅓🅐🅣🅐🅛🅞🅐🅓

#datafromset = Chessset(wechess['AN'])
trainset = Chessset(training_set['AN'], training_set.shape[0])
validset = Chessset(valid_set['AN'], valid_set.shape[0])
testset = Chessset(test_set['AN'], test_set.shape[0])

train_loader = DataLoader(trainset, batch_size = 64, shuffle=True, drop_last=True)
valid_loader = DataLoader(validset, batch_size = 64, shuffle=True, drop_last=True)
test_loader = DataLoader(testset, batch_size = 64, shuffle=True, drop_last=True)

# 🅜🅞🅓🅔🅛
model = QTChessNET()
#model = QTtrgChessNET()

# 🅛🅞🅢🅢
criterion = nn.MSELoss()

# 🅣🅡🅐🅘🅝🅘🅝🅖
train_valid(model, train_loader, valid_loader, criterion)