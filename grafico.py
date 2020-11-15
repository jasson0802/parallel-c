import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import pandas as pd
import numpy as np

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


root = Tk.Tk()
root.wm_title("Coordenadas Paralelas")

df = pd.read_csv('auto.csv')
#df['horsepower'] = pandas.to_numeric(df['horsepower'].replace('?', pandas.nan))
df['mpg'] = pd.cut(df['mpg'], [8, 16, 24, 32, 50])

#plt.rcParams['toolbar'] = 'None'
figura = plt.figure()

canvas = FigureCanvasTkAgg(figura, master=root)
canvas._tkcanvas.pack_forget()
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

print(pd.__version__)
pd.tools.plotting.parallel_coordinates(
    df[['mpg', 'displacement', 'cylinders', 'horsepower', 'weight', 'acceleration']], 
    'mpg')

#plt.show()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()

