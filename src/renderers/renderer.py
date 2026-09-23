import tkinter as tk

class Renderer:
    def __init__(self, canvas, cell_size=20):
        self.canvas = canvas
        self.cell_size = cell_size

    def render(self, model):
        self.canvas.delete("all")
        for r in range(model.rows):
            for c in range(model.cols):
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                
                # Базовый цвет и отрисовка пути/состояний (на основе референса)
                fill_color = "white"
                if (r, c) in model.path:
                    fill_color = "#e500b3"  # Маджента для итогового пути
                elif (r, c) in model.frontier:
                    fill_color = "#c8f4c8"  # Светло-зеленый для текущих (frontier)
                elif (r, c) in model.visited:
                    fill_color = "#f4c8c8"  # Светло-розовый для посещенных

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="#eeeeee")

                # Отрисовка препятствий, старта и финиша
                char = model.grid[r][c]
                if char == '#':
                    # Препятствия как черные точки по референсу
                    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                    rad = self.cell_size * 0.2
                    self.canvas.create_oval(cx - rad, cy - rad, cx + rad, cy + rad, fill="black")
                elif char == 'S':
                    self.canvas.create_text((x0+x1)/2, (y0+y1)/2, text="S", fill="blue", font=("Arial", 10, "bold"))
                elif char == 'E':
                    self.canvas.create_text((x0+x1)/2, (y0+y1)/2, text="E", fill="red", font=("Arial", 10, "bold"))
