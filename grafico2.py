from matplotlib import ticker

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from Tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Tkinter,tkFileDialog
import ttk
from tkcolorpicker import askcolor
from functools import partial
from colormap import rgb2hex
import random

from tkFileDialog import askopenfilename
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def crearListaColore(cantidad):
    lista = []
    for x in range(cantidad):
        tempColor = rgb2hex(random.randint(1, 30)*x, random.randint(1, 30)*x, random.randint(1, 30)*x)
        lista.append(tempColor)
    print lista
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

file = tkFileDialog.askopenfile(master=root,mode='rb',title='Choose a file')
if file != None:
    data = file.read()
    file.close()
    print "I got %d bytes from this file." % len(data)

#Asignar los datos a variable df
global df
df = pd.read_csv(file.name)
#pd.set_option('display.max_columns', None)

#Leer los titulos de las columnas
global cols 
cols = []
for linea in df:
    cols.append(linea)
cols = cols[2:]

categoria = 'mpg'

listaEscala = crearListaEscala(len(cols)+1)

#Reducir valores de columna a evaluar
df[categoria] = pd.cut(df[categoria], listaEscala)

#Asignacion de variables globales

global grosor
grosor = 1.5
#cols = ['displacement', 'cylinders', 'horsepower', 'weight', 'acceleration']
canvas = {}
colores = crearListaColore(len(cols))
min_max_range = {}

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

#Metodo principal donde se dibujan todos los elementos
def dibujar():
    #Asignar los datos a variable df
    global listaEscala
    listaEscala = crearListaEscala(len(cols)+1)
    
    x = [i for i, _ in enumerate(cols)]

    # Crear diccionario de categorias: colores {Interval(24, 32, closed='right'): '#EBD53F', Interval(32, 50, closed='right'): '#9E8F28', Interval(16, 24, closed='right'): '#15D6EB'}
    colours = {df[categoria].cat.categories[i]: colores[i] for i, _ in enumerate(df[categoria].cat.categories)}
    
    fig, axes = plt.subplots(1, len(x)-1, sharey=False, figsize=(15,5))
     
    # Get min, max and range for each column
    # Normalize the data for each column
    for col in cols:
        global min_max_range
        min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))

    # Dibujar cada linea basado en valor de categoria
    for i, ax in enumerate(axes):
        for idx in df.index:
            #Extraer el mpg de la fila
            mpg_category = df.loc[idx, categoria]
            #Dibujar una linea entre cada columna para la fila dada
            ax.plot(x, df.loc[idx, cols],colours[mpg_category],linewidth=grosor) #Aqui se cambia el grueso de la linea
        ax.set_xlim([x[i], x[i+1]])


    # Dibujar escala al lado derecho
    ax = plt.twinx(axes[-1])
    dim = len(axes)
    ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    set_ticks_for_axis(dim, ax, ticks=6)
    ax.set_xticklabels([cols[-2], cols[-1]])
    
    # Quitar espacio entre los dibujos de linea-columna
    plt.subplots_adjust(wspace=0)

    #Creacion componentes tkinter
    plt.rcParams['toolbar'] = 'None'

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas._tkcanvas.pack_forget()
    canvas.draw()

    canvas._tkcanvas.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)

    # Dibujar guia de colores en la parte superior derecha
    plt.legend(
        [plt.Line2D((0,1),(0,0), color=colours[cat]) for cat in df[categoria].cat.categories],
        df[categoria].cat.categories,
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
    botonGrosorLineas= Tk.Button(master=root, text='Cambiar Grosor', command=cambiarGrosor)
    botonGrosorLineas.pack(side=Tk.TOP)
    Ejes = Tk.Label(master=root, text="Ejes")
    Ejes.pack(side=Tk.TOP)
    botonGrosorEjes= Tk.Button(master=root, text='Cambiar Grosor')
    botonGrosorEjes.pack(side=Tk.TOP)
    botonOrdenEjes= Tk.Button(master=root, text='Cambiar orden', command=ventanaOrden)
    botonOrdenEjes.pack(side=Tk.TOP)
    Escala = Tk.Label(master=root, text="Escala")
    Escala.pack(side=Tk.TOP)
    botonEscala= Tk.Button(master=root, text='Cambiar Escala')
    botonEscala.pack(side=Tk.TOP)
    
    botonSalir = Tk.Button(master=root, text='Cerrar', command=_quit)
    botonSalir.pack(side=Tk.TOP)

def cambiarGrosor():
    window = Tk.Toplevel(root)
    w = Spinbox(window,from_=0, to=100)
    w.pack()
    botonAceptar = Tk.Button(window, text='Aceptar', command=partial(aceptar,w))
    botonAceptar.pack()
    
def aceptar(w):
    global grosor
    grosor = w.get()
    limpiarVentana()
    dibujar()
    
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
    df[categoria] = pd.cut(df[categoria], listaEscala)
    if canvas != {}:
        #Si el canvas ya existe borra todos los elementos de tkinter
        for ele in root.winfo_children():
          ele.destroy()
    dibujar()
    
def _quit():
    root.quit()
    root.destroy()

def ventanaOrden():
    posX = 200
    posY = 200
    window = Tk.Toplevel(root)
    window.geometry('1000x500')
    for nombreCol in cols:
        tempLabel = Tk.Label(window,text=nombreCol)
        btnIzq = Tk.Button(window,text="<-" , command = partial(moverIzquierda, nombreCol))
        btnDer = Tk.Button(window,text="->" , command = partial(moverDerecha, nombreCol))
        tempLabel.pack()
        tempLabel.place(x =posX, y = posY)
        btnIzq.place(x =posX-10, y = posY+ 50)
        btnDer.place(x =posX+10, y = posY+ 50);
        posX += 100 


def cambiarColor():
    window = Tk.Toplevel(root)
    Tk.Label(window,text="Colores para rangos de valores de columna " + categoria).grid()
    for rango in listaEscala:
        index = listaEscala.index(rango)
        if(index < len(listaEscala)-1):
            Tk.Label(window,text="Rango " + str(rango) + " - " + str(listaEscala[index+1])).grid()
            Tk.Button(window,text="Cambiar color", command = partial(preguntarColor, rango)).grid()
        

#Se pasa por parametro el nombre de la columna
def preguntarColor(nombreRango):
    #Se busca el indice de la columna
    index = listaEscala.index(nombreRango)
    colorElegido = askcolor((255, 255, 0), parent=root, title="Escoja un color")

    #Se cambia el color en la posicion encontrada por el color elegido
    colores[index] = colorElegido[1]
    
    print(colorElegido)

    limpiarVentana()
    dibujar()


#Se pasa por parametro el nombre de la columna
def moverDerecha(nombreCol):
    #Se busca el indice de la columna
    index = cols.index(nombreCol)

    if index < len(cols)-1:
        tempCol = cols[index+1]
        cols[index+1] = cols[index]
        cols[index] = tempCol
    else:
        tempCol = cols[0]
        cols[0] = cols[index]
        cols[index] = tempCol
    
    print(cols)

    limpiarVentana()
    dibujar()

#Se pasa por parametro el nombre de la columna
def moverIzquierda(nombreCol):
       #Se busca el indice de la columna
    index = cols.index(nombreCol)

    if index > 0:
        tempCol = cols[index-1]
        cols[index-1] = cols[index]
        cols[index] = tempCol
    else:
        tempCol = cols[len(cols)-1]
        cols[len(cols)-1] = cols[index]
        cols[index] = tempCol
    
    print(cols)

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

