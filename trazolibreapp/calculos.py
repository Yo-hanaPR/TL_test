import numpy as np
import matplotlib.pyplot as plt

# Definir los puntos conocidos para cada curva
curvas = {
    "realismo": np.array([[1, 70], [10, 500], [100, 3000]]),
    "logo": np.array([[1, 60], [10, 360], [100, 2100]]),
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

# Función para resolver el sistema de ecuaciones y obtener los coeficientes de la función cuadrática
def obtener_coeficientes(puntos):
    A = np.vstack([puntos[:,0]**2, puntos[:,0], np.ones(len(puntos))]).T
    a, b, c = np.linalg.lstsq(A, puntos[:,1], rcond=None)[0]
    return a, b, c

# Función para obtener la función cuadrática a partir de los coeficientes
def funcion_cuadratica(a, b, c):
    return lambda x: a*x**2 + b*x + c

# Crear la figura y el eje
fig, ax = plt.subplots()
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
    x_valores = np.linspace(0, 10, 1000)  # Cambiado a 10 metros
    y_valores = funcion(x_valores)
    line.set_data(x_valores, y_valores)
    line.set_color(colors[curva])  # Asignar color correspondiente a la curva
    ax.set_title(f'Curva: {curva.capitalize()}')
    
    # Ajustar los límites de los ejes x e y
    ax.set_xlim(0, 10)  # Cambiado a 10 metros
    ax.set_ylim(0, 3000)  # Establecer límite superior de y en 3000 para todas las curvas
    
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
from matplotlib.widgets import Button
botones = []
for i, curva in enumerate(curvas.keys()):
    boton = Button(plt.axes([0.1 + i*0.12, 0.02, 0.1, 0.05]), curva.capitalize(), color=colors[curva])
    boton.on_clicked(lambda event, nombre_curva=curva: cambiar_curva(nombre_curva))
    botones.append(boton)

# Añadir una casilla de entrada para los metros cuadrados
from matplotlib.widgets import TextBox
def calcular(event):
    metros_cuadrados = float(text_box.text)
    y = funcion_cuadratica(a, b, c)(metros_cuadrados)
    categoria_texto.set_text(f'Categoría: {curva_actual.capitalize()}')
    coordenadas_texto.set_text(f'Metros cuadrados: {metros_cuadrados:.2f}\nDólares: {y:.2f}')
    fig.canvas.draw_idle()

text_box = TextBox(plt.axes([0.35, 0.2, 0.3, 0.05]), 'Metros cuadrados')
text_box.on_submit(calcular)

# Configuración adicional del gráfico
ax.set_xlabel('Metros cuadrados')
ax.set_ylabel('Dólares')
ax.grid(True)

# Mostrar el gráfico
plt.show()