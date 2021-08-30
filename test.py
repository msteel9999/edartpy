import numpy as np
import pandas as pd

a = [1, 2, 3, 4, 5]
a = pd.DataFrame(a)
print(np.shape(a)[0])
print(a)
a = a.iloc[0:]
print(a)