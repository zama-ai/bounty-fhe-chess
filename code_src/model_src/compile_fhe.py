import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import sys
from tqdm import tqdm

from concrete.ml.torch.compile import compile_brevitas_qat_model

#from code_src.model_src.dataset_source import Chessset
from dataset_source import Chessset
#from dataset_target import Chessset

# CLEAR #
# sys.path.insert(1,"code_src/model_src/clear/")

# source
# from train_v3_source_clear import test
# from cnn_v13_64bit_source_clear import PlainChessNET

# target
# from train_v3_target import test
# from cnn_v13_64bit_target_unfhe import PlainChessNET

# QUANTIZED #
sys.path.insert(1,"code_src/model_src/quantz/")

# source
from test_source_FHE import test_with_concrete
from source_44cnn_quantz import QTChessNET

# quantized - target
# from test_target_FHE import test_with_concrete
# from target_44cnn_quantz import QTtrgChessNET


"""
LOADING SECTION
training_set = Chessset(dataset['AN'])
"""
#       ___           ___           ___                   ___                    ___           ___           ___           ___     
#      /\  \         /\  \         /\__\      ___        /\  \                  /\  \         /\  \         /\  \         /\  \    
#     /::\  \       /::\  \       /:/  /     /\  \       \:\  \                /::\  \       /::\  \        \:\  \       /::\  \   
#    /:/\ \  \     /:/\:\  \     /:/  /      \:\  \       \:\  \              /:/\:\  \     /:/\:\  \        \:\  \     /:/\:\  \  
#   _\:\~\ \  \   /::\~\:\  \   /:/  /       /::\__\      /::\  \            /:/  \:\__\   /::\~\:\  \       /::\  \   /::\~\:\  \ 
#  /\ \:\ \ \__\ /:/\:\ \:\__\ /:/__/     __/:/\/__/     /:/\:\__\          /:/__/ \:|__| /:/\:\ \:\__\     /:/\:\__\ /:/\:\ \:\__\
#  \:\ \:\ \/__/ \/__\:\/:/  / \:\  \    /\/:/  /       /:/  \/__/          \:\  \ /:/  / \/__\:\/:/  /    /:/  \/__/ \/__\:\/:/  /
#   \:\ \:\__\        \::/  /   \:\  \   \::/__/       /:/  /                \:\  /:/  /       \::/  /    /:/  /           \::/  / 
#    \:\/:/  /         \/__/     \:\  \   \:\__\       \/__/                  \:\/:/  /        /:/  /     \/__/            /:/  /  
#     \::/  /                     \:\__\   \/__/                               \::/__/        /:/  /                      /:/  /   
#      \/__/                       \/__/                                        ~~            \/__/                       \/__/    


game_move_set = "data/wb_2000_300.csv"
wechess = pd.read_csv(game_move_set)

# split dataset splitted into: training_set (80%), valid_set (20%), test_set (20%)
#training_set, valid_set, test_set = np.split(wechess.sample(frac=1, random_state=42), [int(.6*len(wechess)), int(.8*len(wechess))])

# IMPORTANT downsizing the training set size to avoid crash causes by overload computation
training_set, valid_set, test_set = np.split(wechess.sample(frac=1, random_state=42), [int(.0005*len(wechess)), int(.8*len(wechess))])

print(f"When compiling with concrete-ml, tthe size of training_set should be at least 100 data points, here: {len(training_set)}.")

#      ___           ___           ___           ___           ___       ___           ___           ___     
#     /\  \         /\  \         /\  \         /\  \         /\__\     /\  \         /\  \         /\  \    
#    /::\  \       /::\  \        \:\  \       /::\  \       /:/  /    /::\  \       /::\  \       /::\  \   
#   /:/\:\  \     /:/\:\  \        \:\  \     /:/\:\  \     /:/  /    /:/\:\  \     /:/\:\  \     /:/\:\  \  
#  /:/  \:\__\   /::\~\:\  \       /::\  \   /::\~\:\  \   /:/  /    /:/  \:\  \   /::\~\:\  \   /:/  \:\__\ 
# /:/__/ \:|__| /:/\:\ \:\__\     /:/\:\__\ /:/\:\ \:\__\ /:/__/    /:/__/ \:\__\ /:/\:\ \:\__\ /:/__/ \:|__|
# \:\  \ /:/  / \/__\:\/:/  /    /:/  \/__/ \/__\:\/:/  / \:\  \    \:\  \ /:/  / \/__\:\/:/  / \:\  \ /:/  /
#  \:\  /:/  /       \::/  /    /:/  /           \::/  /   \:\  \    \:\  /:/  /       \::/  /   \:\  /:/  / 
#   \:\/:/  /        /:/  /     \/__/            /:/  /     \:\  \    \:\/:/  /        /:/  /     \:\/:/  /  
#    \::/__/        /:/  /                      /:/  /       \:\__\    \::/  /        /:/  /       \::/__/   
#     ~~            \/__/                       \/__/         \/__/     \/__/         \/__/         ~~       

# from dataset through Chessset class
trainset = Chessset(training_set['AN'], training_set.shape[0])
validset = Chessset(valid_set['AN'], valid_set.shape[0])
testset = Chessset(test_set['AN'], test_set.shape[0])

# from Chessset class through torch Dataloader
train_loader = DataLoader(trainset, batch_size = 64, shuffle=True, drop_last=True)
valid_loader = DataLoader(validset, batch_size = 64, shuffle=True, drop_last=True)
test_loader = DataLoader(testset, batch_size = 1, shuffle=True, drop_last=True)

# model instantiation zone

# quantized model 1 - aka source  
model = QTChessNET()

# quantized model 2 - aka target
#model = QTtrgChessNET()

# loss
criterion = nn.MSELoss()

## TESTING and ACCURACY

# defining the processor
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# loading zone
# quantized model 1 - aka source  
model.load_state_dict(torch.load("server/model/source_model_quant44.pt",map_location = device))

# quantized model 2 - aka target
#model.load_state_dict(torch.load("server/model/target_model_quant44.pt",map_location = device))

model.pruning_conv(False)

## Prepare train_input data for compilation with concrete-ml

"""
reminder
model 1 (source): from input data (chessboard) predict selected square to be played (source)
model 1 (source): from input data (tuple (chessboard source)) predict selected square to be played (target)
"""

def get_train_input(trainload_set, target=False):
    
    """If target=True, Concrete-ml compiles model 2 (target), otherwise model 1 (source).
    
    Goal: returning train_input as:
        - array of tensor (mono input_data)
        - tuple of arrays of tensor (multiple input_datas).
    """

    list_train_inputs = []
    list_train_sources = []

    if target:
        # TARGET CASE
        # preparation training input_data: chessboard, source
        loop_trainset = tqdm(enumerate(trainload_set), total=len(trainload_set), leave=False)

        for idx, (chessboard, sources, targets) in loop_trainset:
            data, source, target = chessboard.clone().detach().float(),  sources.clone().detach().float(), targets.clone().detach().float() #torch.tensor(chessboard).float(), torch.tensor(targets).float() # 

            list_train_inputs.append(data)
            list_train_sources.append(source)

        loop_trainset.set_description(f"datasss [{idx}/{trainload_set}]")

        train_chess = np.concatenate(list_train_inputs)
        train_source = np.concatenate(list_train_sources)

        train_input = (train_chess, train_source)
        return train_input
    
    else:
        # SOURCE CASE
        # preparation training input_data: chessboard
        loop_trainset = tqdm(enumerate(trainload_set), total=len(trainload_set), leave=False)

        for idx, (chessboard, targets) in loop_trainset:
            data, target = chessboard.clone().detach().float(), targets.clone().detach().float()
            list_train_sources.append(data)

        loop_trainset.set_description(f"datasss [{idx}/{trainload_set}]")

        train_input = np.concatenate(list_train_sources, axis=0)
        return train_input


# instantiate the train_loader (as array of tensor) as train_input
train_input = get_train_input(train_loader, target=False)

#1 Compile to FHE
print("Concrete-ml is compiling")

start_compile = time.time()

q_module_vl = compile_brevitas_qat_model(model, train_input, n_bits={"model_inputs":4, "model_outputs":4})

end_compile = time.time()

print(f"Compilation finished in {end_compile - start_compile:.2f} seconds")

#2 Check that the network is compatible with FHE constraints
print("checking FHE constraints compatibility")

bitwidth = q_module_vl.fhe_circuit.graph.maximum_integer_bit_width()
print(
    f"Max bit-width: {bitwidth} bits" + " -> it works in FHE!!"
    if bitwidth <= 16
    else f"{bitwidth} bits too high for FHE computation"
)

#3 test concrete and monitoring accuracy
print("Test with concrete")
start_time_encrypt = time.time()

test_with_concrete(q_module_vl,test_loader)
print("Time per inference under FHE context:", (time.time()-start_time_encrypt/len(test_loader)))