import os 
import glob 

INPUT_PATH = 'inputs/'
INPUTS = list(glob.glob(os.path.join(INPUT_PATH, "*.txt")))

with open(INPUTS[0]) as f:
    lines = f.readlines()
    print(type(lines))
    print(lines)