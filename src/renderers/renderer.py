import tkinter as tk

class Renderer:
    def __init__(self, canvas, cell_size=12):
        self.canvas = canvas
        self.cell_size = cell_size

    def render(self, model):
        self.canvas.delete("all")
        
        # 1. Отрисовка клеток (без границ)
        for r in range(model.rows):
            for c in range(model.cols):
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                
                if (r, c) in model.frontier:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#c8f4c8", outline="")
                elif (r, c) in model.visited:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#f2b6b6", outline="")
                
                char = model.grid[r][c]
                if char == '#':
                    # Препятствия как мелкие черные квадратики в центре
                    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                    rad = self.cell_size * 0.25
                    self.canvas.create_rectangle(cx - rad, cy - rad, cx + rad, cy + rad, fill="#222222", outline="")

        # 2. Отрисовка непрерывной линии пути (динамической)
        path = model.get_current_path()
        if len(path) > 1:
            line_coords = []
            for r, c in path:
                cx = c * self.cell_size + self.cell_size / 2
                cy = r * self.cell_size + self.cell_size / 2
                line_coords.extend([cx, cy])
            # Рисуем толстую пурпурную линию со скругленными углами
            self.canvas.create_line(*line_coords, fill="#d800d8", width=3, joinstyle=tk.ROUND, capstyle=tk.ROUND)

        # 3. Отрисовка Старта и Финиша (небольшие круги)
        if model.start and model.end:
            sr, sc = model.start
            er, ec = model.end
            sx, sy = sc * self.cell_size + self.cell_size / 2, sr * self.cell_size + self.cell_size / 2
            ex, ey = ec * self.cell_size + self.cell_size / 2, er * self.cell_size + self.cell_size / 2
            self.canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4, fill="blue", outline="")
            self.canvas.create_oval(ex - 4, ey - 4, ex + 4, ey + 4, fill="red", outline="")
