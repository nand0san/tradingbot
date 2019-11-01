import numpy as np

# 1d array to list
arr = np.array([1, 2, 3])
arr = arr[1:]
print(f'NumPy Array:\n{arr}')

list1 = arr.tolist()
print(f'List: {list1}')
