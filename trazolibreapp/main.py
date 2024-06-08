import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class ImagePlacerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plano Cartesiano con Imágenes")
        self.geometry("800x600")
        self.canvas = None
        self.ax = None
        self.current_image = None
        self.drag_data = {"x": 0, "y": 0, "item": None}

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
            image = Image.open(filename)
            image = image.resize((40, 40))  # Redimensionar a 100x100
            image = ImageTk.PhotoImage(image)
            self.current_image = image
            self.ax.imshow(image, extent=(2, 7, 2, 7))
            self.canvas.draw()


    def on_press(self, event):
        if event.inaxes is not None and self.current_image is not None:
            x, y = event.xdata, event.ydata
            if 2 < x < 7 and 2 < y < 7:
                self.drag_data["x"] = x
                self.drag_data["y"] = y
                self.drag_data["item"] = self.current_image

    def on_release(self, event):
        self.drag_data["item"] = None

    def on_motion(self, event):
        if self.drag_data["item"] is not None:
            dx = event.xdata - self.drag_data["x"]
            dy = event.ydata - self.drag_data["y"]
            self.ax.images.remove(self.drag_data["item"])
            self.drag_data["item"] = self.ax.imshow(self.current_image, extent=(2 + dx, 7 + dx, 2 + dy, 7 + dy))
            self.canvas.draw()

if __name__ == "__main__":
    app = ImagePlacerApp()
    app.mainloop()
