import pickle
import os
if os.path.exists('msgStg.txt') and os.path.getsize('msgStg.txt') > 0:
    with open('msgStg.txt', "rb") as f:
        data = pickle.load(f)
        print(data)
else:
    print("File empty or not found.")