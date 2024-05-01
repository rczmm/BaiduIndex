import numpy as np

values = [np.random.randint(0, 100) for i in range(100)]
print(values)
print(type(values))

values = np.array(values)
min_value = np.min(values)
max_value = np.max(values)