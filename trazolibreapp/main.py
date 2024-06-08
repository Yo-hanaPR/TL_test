import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import numpy as np

class ImagePlacerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plano Cartesiano con Imágenes")
        self.geometry("800x600")
        self.canvas = None
        self.ax = None
        self.current_image = None
        self.drag_data = {"x": 0, "y": 0, "item": None, "action": None}
        self.images = []  # Lista para almacenar las imágenes y sus posiciones

        self.create_widgets()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.create_cartesian_plane()

        upload_button = tk.Button(self, text="Cargar Imagen", command=self.upload_image)
        upload_button.pack(side=tk.BOTTOM)

    def create_cartesian_plane(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def upload_image(self):
        filename = filedialog.askopenfilename()
        if filename:
            print("Ruta de la imagen:", filename)  # Imprimir la ruta de la imagen
            image = Image.open(filename)
            image = image.resize((100, 100))  # Redimensionar a 100x100
            print("Imagen redimensionada:", image)  # Imprimir la imagen redimensionada
            
            # Convertir la imagen a un arreglo NumPy
            image_array = np.array(image)


            
            # Mostrar la imagen en el plano cartesiano
            img_obj = self.ax.imshow(image_array, extent=(2, 7, 2, 7))
            
            # Guardar la imagen y su objeto gráfico en la lista de imágenes
            self.images.append({"image": image, "extent": [2, 7, 2, 7], "obj": img_obj})
            self.canvas.draw()

    def on_press(self, event):
        if event.inaxes is not None:
            for img in self.images:
                x0, x1, y0, y1 = img["extent"]
                if x0 <= event.xdata <= x1 and y0 <= event.ydata <= y1:
                    if abs(event.xdata - x1) < 0.2 and abs(event.ydata - y1) < 0.2:
                        self.drag_data["action"] = "resize"
                    else:
                        self.drag_data["action"] = "move"
                    self.drag_data["item"] = img
                    self.drag_data["x"] = event.xdata
                    self.drag_data["y"] = event.ydata
                    break


    def on_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["action"] = None

    def on_motion(self, event):
        if self.drag_data["item"] is not None and event.inaxes is not None:
            dx = event.xdata - self.drag_data["x"]
            dy = event.ydata - self.drag_data["y"]
            img = self.drag_data["item"]
            x0, x1, y0, y1 = img["extent"]
            
            if self.drag_data["action"] == "move":
                new_extent = [x0 + dx, x1 + dx, y0 + dy, y1 + dy]
            elif self.drag_data["action"] == "resize":
                new_extent = [x0, x0 + (x1 - x0) + dx, y0, y0 + (y1 - y0) + dy]
            
            img["extent"] = new_extent
            img["obj"].set_extent(new_extent)
            self.drag_data["x"] = event.xdata
            self.drag_data["y"] = event.ydata
            self.canvas.draw()

if __name__ == "__main__":
    app = ImagePlacerApp()
    app.mainloop()
