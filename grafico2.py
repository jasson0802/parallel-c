from matplotlib import ticker

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Tkinter,tkFileDialog
import ttk
from tkcolorpicker import askcolor
from functools import partial

from tkFileDialog import askopenfilename
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def crearListaColore(cantidad):
    lista = []
    if(cantidad == 6):
        lista=['#0097FF','#00E4FF', '#00FFDC', '#00FF63', '#C9FF00','#0097FF']
    elif(cantidad == 5):
        lista=['#2F939E','#EB0E87', '#15D6EB', '#EBD53F', '#9E8F28']
    elif(cantidad == 4):
        lista=['#2F939E','#EB0E87', '#15D6EB', '#EBD53F']
    elif(cantidad == 3):
        lista=['#2F939E','#EB0E87', '#15D6EB']
    elif(cantidad == 2):
        lista=['#2F939E','#EB0E87']
    elif(cantidad == 1):
        lista=['#2F939E']
    return lista
def crearListaEscala(cantidad):
    lista=[]
    if(cantidad == 7):
        lista=[0,8, 16, 24, 32, 50,60]
    elif(cantidad == 6):
        lista=[0,8, 16, 24, 32, 50]
    elif(cantidad == 5):
        lista=[0,8, 16, 24, 32, 50]
    return lista
#Creacion de ventana tkinter
root = Tk.Tk()
root.wm_title("Coordenadas Paralelas")
#root.style = ttk.Style()
#root.style.theme_use("vista")

file = tkFileDialog.askopenfile(master=root,mode='rb',title='Choose a file')
if file != None:
    data = file.read()
    file.close()
    print "I got %d bytes from this file." % len(data)
df = pd.read_csv(file.name)
#Leer los titulos de las columnas
global cols 
cols = []
for linea in df:
    cols.append(linea)
cols = cols[2:]
#df['horsepower'] = pd.to_numeric(df['horsepower'].replace('?', np.nan))
listaEscala = crearListaEscala(len(cols)+1)
df['mpg'] = pd.cut(df['mpg'], listaEscala)



#Asignacion de variables globales
min_max_range = {}
#cols = ['displacement', 'cylinders', 'horsepower', 'weight', 'acceleration']
canvas = {}
colores = crearListaColore(len(cols))
# Set the tick positions and labels on y axis for each plot
# Tick positions based on normalised data
# Tick labels are based on original data
def set_ticks_for_axis(dim, ax, ticks):
    min_val, max_val, val_range = min_max_range[cols[dim]]
    step = val_range / float(ticks-1)
    tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
    norm_min = df[cols[dim]].min()
    norm_range = np.ptp(df[cols[dim]])
    norm_step = norm_range / float(ticks-1)
    ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
    ax.yaxis.set_ticks(ticks)
    ax.set_yticklabels(tick_labels)


#plt.title("Values of car attributes by MPG category")
#plt.show()

#Metodo principal donde se dibujan todos los elementos
def dibujar(columnas = cols):
    cols = columnas
    x = [i for i, _ in enumerate(cols)]
    colours = colores

    # create dict of categories: colours
    colours = {df['mpg'].cat.categories[i]: colours[i] for i, _ in enumerate(df['mpg'].cat.categories)}
    
    fig, axes = plt.subplots(1, len(x)-1, sharey=False, figsize=(15,5))
     
    # Create (X-1) sublots along x axis
    #fig, axes = plt.subplots()

    # Get min, max and range for each column
    # Normalize the data for each column
    for col in cols:
        global min_max_range
        min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))

    # Plot each row
    for i, ax in enumerate(axes):
        for idx in df.index:
            mpg_category = df.loc[idx, 'mpg']
            ax.plot(x, df.loc[idx, cols],colours[mpg_category],linewidth=0.5) #Aqui se cambia el grueso de la linea
        ax.set_xlim([x[i], x[i+1]])


    # Move the final axis' ticks to the right-hand side
    ax = plt.twinx(axes[-1])
    dim = len(axes)
    ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    set_ticks_for_axis(dim, ax, ticks=6)
    ax.set_xticklabels([cols[-2], cols[-1]])
    # Remove space between subplots
    plt.subplots_adjust(wspace=0)

    #Creacion componentes tkinter

    plt.rcParams['toolbar'] = 'None'

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas._tkcanvas.pack_forget()
    canvas.draw()
    #canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    #toolbar = NavigationToolbar2TkAgg(canvas, root)
    #toolbar.update()

    canvas._tkcanvas.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)

    # Add legend to plot
    plt.legend(
        [plt.Line2D((0,1),(0,0), color=colours[cat]) for cat in df['mpg'].cat.categories],
        df['mpg'].cat.categories,
        bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=0.)

    for dim, ax in enumerate(axes):
        ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
        set_ticks_for_axis(dim, ax, ticks=6)
        ax.set_xticklabels([cols[dim]])

    #Dibujar botones 
    botonCargarArchivo = Tk.Button(master=root, text='Abrir Archivo', command=cargar_archivo)
    botonCargarArchivo.pack(side=Tk.TOP)   
    lineas = Tk.Label(master=root, text="Lineas")
    lineas.pack(side=Tk.TOP)    
    botonColorLineas = Tk.Button(master=root, text='Cambiar Color', command=cambiarColor)
    botonColorLineas.pack(side=Tk.TOP)
    botonGrosorLineas= Tk.Button(master=root, text='Cambiar Grosor')
    botonGrosorLineas.pack(side=Tk.TOP)
    Ejes = Tk.Label(master=root, text="Ejes")
    Ejes.pack(side=Tk.TOP)
    botonGrosorEjes= Tk.Button(master=root, text='Cambiar Grosor')
    botonGrosorEjes.pack(side=Tk.TOP)
    Escala = Tk.Label(master=root, text="Escala")
    Escala.pack(side=Tk.TOP)
    botonEscala= Tk.Button(master=root, text='Cambiar Escala')
    botonEscala.pack(side=Tk.TOP)
    
    botonSalir = Tk.Button(master=root, text='Cerrar', command=_quit)
    botonSalir.pack(side=Tk.TOP)

def cargar_archivo():
    file = tkFileDialog.askopenfile(master=root,mode='rb',title='Choose a file')
    if file != None:
           data = file.read()
           file.close()
           print "I got %d bytes from this file." % len(data)

    global df
    df = pd.read_csv(file.name)
    #df['horsepower'] = pd.to_numeric(df['horsepower'].replace('?', np.nan))
    cols = []
    for linea in df:
        cols.append(linea)
    cols = cols[2:]
    listaEscala = crearListaEscala(len(cols)+1)
    df['mpg'] = pd.cut(df['mpg'],listaEscala)
    if canvas != {}:
        #Si el canvas ya existe borra todos los elementos de tkinter
        for ele in root.winfo_children():
          ele.destroy()
    dibujar()
    
def _quit():
    root.quit()
    root.destroy()

def cambiarColor():
    window = Tk.Toplevel(root)
    for nombreCol in cols:
        Tk.Label(window,text=nombreCol).grid()
        Tk.Button(window,text="Cambiar: " + nombreCol, command = partial(preguntarColor, nombreCol) ).grid()


#Se pasa por parametro el nombre de la columna
def preguntarColor(nombreCol):
    #Se busca el indice de la columna
    index = cols.index(nombreCol)
    colorElegido = askcolor((255, 255, 0), parent=root, title="Escoja un color")

    #Se cambia el color en la posicion encontrada por el color elegido
    colores[index] = colorElegido[1]
    
    print(colorElegido)

    limpiarVentana()
    dibujar()


def limpiarVentana():
    for ele in root.winfo_children():
          ele.destroy()
    
#Metodo para cambiar colores
def actualizarColor():
    #Valida si el canvas ya existe
    if canvas != {}:
        #Si el canvas ya existe borra todos los elementos de tkinter
        limpiarVentana()

        #Resetea los colores
        global colores
        colores = crearListaColore(len(cols))

        #Vuelve a generar todos los elementos
        dibujar()

#Incializa 
dibujar()

#Proceso principal de tkinter
Tk.mainloop()

