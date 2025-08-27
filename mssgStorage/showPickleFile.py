import pickle
import os
if os.path.exists('msgStg.txt') and os.path.getsize('msgStg.txt') > 0:
    with open('msgStg.txt', "rb") as f:
        data = pickle.load(f)
        lastId = list(data.keys())[len(data) - 1]
        print(lastId)
else:
    print("File empty or not found.")