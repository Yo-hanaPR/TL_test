import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import numpy as np

class PolygonDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dibujo de Polígonos")
        
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()
        
        self.points = []
        self.polygon = None
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.button == 1:  # Left click to add points
            self.points.append((event.xdata, event.ydata))
            self.draw_polygon()
        elif event.button == 3:  # Right click to close polygon
            if len(self.points) > 2:
                self.points.append(self.points[0])  # Close the polygon
                self.draw_polygon()
                self.points = []

    def draw_polygon(self):
        if self.polygon:
            self.polygon.remove()
        if len(self.points) > 1:
            self.polygon = Polygon(np.array(self.points), closed=False, fill=None, edgecolor='black')
            self.ax.add_patch(self.polygon)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonDrawer(root)
    root.mainloop()
