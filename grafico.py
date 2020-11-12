import matplotlib.pyplot as plt


import pandas as pd
import numpy as np

df = pd.read_csv('auto.csv')
#df['horsepower'] = pandas.to_numeric(df['horsepower'].replace('?', pandas.nan))
df['mpg'] = pd.cut(df['mpg'], [8, 16, 24, 32, 50])

plt.figure()
print(pd.__version__)
pd.tools.plotting.parallel_coordinates(
    df[['mpg', 'displacement', 'cylinders', 'horsepower', 'weight', 'acceleration']], 
    'mpg')


plt.show()
