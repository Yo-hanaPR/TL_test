import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter import filedialog
from PIL import Image
import tkinter as tk
from tkinter import ttk
from matplotlib.patches import Polygon
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

# Definir los puntos conocidos para cada curva
curvas = {
    "realismo": np.array([[1, 70], [10, 500], [100, 3000]]),
    "logo": np.array([[1, 60], [10, 440], [100, 2400]]),
    "comic": np.array([[1, 50], [10, 310], [100, 1800]]),
    "lettering": np.array([[1, 40], [10, 260], [100, 1500]]),
    "minimalismo": np.array([[1, 30], [10, 210], [100, 1200]]),
    "abstracto": np.array([[1, 20], [10, 170], [100, 800]])
}

# Colores para cada curva
colors = {
    "realismo": 'blue',
    "logo": 'red',
    "comic": 'green',
    "lettering": 'orange',
    "minimalismo": 'purple',
    "abstracto": 'cyan'
}



class PolygonDrawer:
    def __init__(self, ax):
        self.ax = ax
        self.polylines = []
        self.current_polyline = None
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_click)
    def caja_texto(self):
       print("Hello")
       TextBox(plt.axes([0.25, 0.5, 0.3, 0.05]), 'Figura')
        

    def on_click(self, event):
        if event.button == 1:  # Left click to add points
            if self.current_polyline is None:
                self.current_polyline, = self.ax.plot([], [], color='black')
                self.polylines.append(self.current_polyline)
            if len(self.current_polyline.get_xdata()) > 0:
                last_point = np.array([self.current_polyline.get_xdata()[-1], self.current_polyline.get_ydata()[-1]])
                new_point = np.array([event.xdata, event.ydata])
                distance = np.linalg.norm(new_point - last_point)
                if distance <= 0.010:  # Check if new point is close enough to close the polygon
                ## Hacer doble click para cerrar el polígono
                    self.current_polyline.set_xdata(list(self.current_polyline.get_xdata()) + [self.current_polyline.get_xdata()[0]])
                    self.current_polyline.set_ydata(list(self.current_polyline.get_ydata()) + [self.current_polyline.get_ydata()[0]])
                    self.current_polyline = None
                    self.caja_texto()
                else:
                    self.current_polyline.set_xdata(list(self.current_polyline.get_xdata()) + [event.xdata])
                    self.current_polyline.set_ydata(list(self.current_polyline.get_ydata()) + [event.ydata])
            else:
                # Primer punto del polígono
                self.current_polyline.set_xdata([event.xdata])
                self.current_polyline.set_ydata([event.ydata])
            self.ax.figure.canvas.draw()

    def reset_polygon(self):
        if self.current_polyline:
            self.current_polyline.remove()
            self.current_polyline = None
        for line in self.polylines:
            line.remove()
        self.polylines = []
        self.ax.figure.canvas.draw()

############### Cierre clase PolygonDrawer##########

# Función para resolver el sistema de ecuaciones y obtener los coeficientes de la función cuadrática
def obtener_coeficientes(puntos):
    A = np.vstack([puntos[:,0]**2, puntos[:,0], np.ones(len(puntos))]).T
    a, b, c = np.linalg.lstsq(A, puntos[:,1], rcond=None)[0]
    return a, b, c

# Función para obtener la función cuadrática a partir de los coeficientes
def funcion_cuadratica(a, b, c):
    return lambda x: a*x**2 + b*x + c

# Crear la figura del plano y el eje
fig, ax = plt.subplots()
fig.set_size_inches(10, 8) #hace que la ventana sea mas grande
fig.subplots_adjust(bottom=0.35)

# Inicializar una línea vacía en el eje
line, = ax.plot([], [], label='Curva')

# Cuadro de texto para mostrar las coordenadas al hacer clic
coordenadas_texto = ax.text(0.5, 0.1, '', transform=ax.transAxes, fontsize=10)
categoria_texto = ax.text(0.5, 0.9, '', transform=ax.transAxes, fontsize=10)

# Variables globales para los coeficientes de la función cuadrática
a, b, c = obtener_coeficientes(curvas["realismo"])

# Función para actualizar el gráfico con la curva seleccionada
def actualizar_curva(curva):
    global a, b, c
    puntos = curvas[curva]
    a, b, c = obtener_coeficientes(puntos)
    funcion = funcion_cuadratica(a, b, c)
    x_valores = np.linspace(0, 10, 1000)
    y_valores = funcion(x_valores)
    line.set_data(x_valores, y_valores)
    line.set_color(colors[curva])  # Asignar color correspondiente a la curva
    ax.set_title(f'Curva: {curva.capitalize()}')
    
    # Ajustar los límites de los ejes x e y
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3000)
    
    fig.canvas.draw()

# Inicializar el gráfico con la primera curva
curva_actual = "realismo"
actualizar_curva(curva_actual)

# Función para manejar el evento de clic en los botones de categoría
def cambiar_curva(nombre_curva):
    global curva_actual
    curva_actual = nombre_curva
    categoria_texto.set_text('')
    coordenadas_texto.set_text('')
    actualizar_curva(curva_actual)
    ax.set_title(f'Curva: {curva_actual.capitalize()}')

# Crear y posicionar los botones de categoría
botones = []
for i, curva in enumerate(curvas.keys()):
    boton = Button(plt.axes([0.1 + i*0.12, 0.02, 0.1, 0.05]), curva.capitalize(), color=colors[curva])
    boton.on_clicked(lambda event, nombre_curva=curva: cambiar_curva(nombre_curva))
    botones.append(boton)

# Añadir una casilla de entrada para los metros cuadrados
def calcular(event):
    metros_cuadrados = float(text_box.text)
    y = funcion_cuadratica(a, b, c)(metros_cuadrados)
    categoria_texto.set_text(f'Categoría: {curva_actual.capitalize()}')
    coordenadas_texto.set_text(f'Metros cuadrados: {metros_cuadrados:.2f}\nDólares: {y:.2f}')
    fig.canvas.draw_idle()

text_box = TextBox(plt.axes([0.35, 0.2, 0.3, 0.05]), 'Metros cuadrados')
text_box.on_submit(calcular)

# Clase para manejar la imagen
class DraggableImage:
    def __init__(self, ax, img_array):
        self.ax = ax
        self.image = OffsetImage(img_array, zoom=0.5)
        self.ab = AnnotationBbox(self.image, (5, 1500), xycoords='data', frameon=False)
        self.ax.add_artist(self.ab)
        self.press = None
        self.background = None
        self.cidpress = self.ab.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.ab.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.ab.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cidscroll = self.ab.figure.canvas.mpl_connect('scroll_event', self.on_scroll)

    def on_press(self, event):
        print("paso por aqui")
        if event.inaxes != self.ab.axes: return
        contains, attrd = self.ab.contains(event)
        if not contains: return
        self.press = self.ab.xy, event.xdata, event.ydata

    def on_release(self, event):
        self.press = None
        self.ab.figure.canvas.draw()

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.ab.axes: return
        (x0, y0), xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.ab.xy = (x0 + dx, y0 + dy)
        self.ab.figure.canvas.draw()

    def on_scroll(self, event):
        if event.inaxes != self.ab.axes: return
        zoom = 1.2 if event.button == 'up' else 0.8
        curr_zoom = self.image.get_zoom()
        new_zoom = curr_zoom * zoom
        self.image.set_zoom(new_zoom)
        self.ab.figure.canvas.draw()

# Añadir un botón para cargar la imagen
def cargar_imagen(event):
    filename = filedialog.askopenfilename()
    if filename:
        print("Ruta de la imagen:", filename)
        image = Image.open(filename)
        image = image.resize((100, 100))
        print("Imagen redimensionada:", image)
        
        # Convertir la imagen a un arreglo NumPy
        image_array = np.array(image)
        
        # Mostrar la imagen en el plano cartesiano
        img_obj = DraggableImage(ax, image_array)
        img_obj.on_press(event)
        img_obj.on_motion(event)
        # Restablecer los límites de los ejes después de mostrar la imagen
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3000)
        
        fig.canvas.draw()

# Crear y posicionar el botón para cargar la imagen
cargar_imagen_button = Button(plt.axes([0.8, 0.02, 0.2, 0.05]), "Cargar Imagen")
cargar_imagen_button.on_clicked(cargar_imagen)

# Configuración adicional del gráfico
ax.set_xlabel('Metros cuadrados')
ax.set_ylabel('Dólares')
ax.grid(True)

# Variables para almacenar el punto inicial del vector
start_point = None
vector = None

# Funciones para manejar los eventos del ratón
def on_click(event):
    global start_point, vector
    if event.inaxes != ax:
        return
    if event.button == 1:  # Click izquierdo
        start_point = (event.xdata, event.ydata)
        if vector:
            vector.remove()
            vector = None

def on_release(event):
    global start_point, vector
    if event.inaxes != ax or start_point is None:
        return
    if event.button == 1:  # Click izquierdo
        end_point = (event.xdata, event.ydata)
        #vector = ax.arrow(start_point[0], start_point[1], end_point[0] - start_point[0], end_point[1] - start_point[1], head_width=0.5, head_length=1, fc='k', ec='k')
        fig.canvas.draw()
        start_point = None

# Conectar los eventos de ratón a las funciones correspondientes
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('button_release_event', on_release)

# Mostrar el gráfico

polygon_drawer = PolygonDrawer(ax)

plt.show()
