import json
import os
from flatten import flatten


path = './files'

data = []
for file in os.listdir(path):
    with open(path+'/'+file, encoding='utf-8') as f:
        data.append(flatten(json.load(f)))
