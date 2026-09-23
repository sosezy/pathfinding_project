import tkinter as tk
from tkinter import filedialog
from src.models.grid_model import GridModel
from src.renderers.renderer import Renderer

class App:
    def __init__(self, width=800, height=700):
        self.root = tk.Tk()
        self.root.title("Поиск пути: A* и Дейкстра")
        
        self.control_frame = tk.Frame(self.root, pady=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(self.control_frame, text="Загрузить лабиринт", command=self.load_maze).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Старт A*", command=lambda: self.start_algo("A*")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Старт Дейкстра", command=lambda: self.start_algo("Dijkstra")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="Очистить пути", command=self.clear_paths).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, width=width, height=height-50, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.model = GridModel(25, 35)
        self.renderer = Renderer(self.canvas, cell_size=20)
        
        self.algo_generator = None
        self.renderer.render(self.model)

    def load_maze(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            self.model.load_from_file(filepath)
            self.renderer.render(self.model)

    def start_algo(self, algo_type):
        self.algo_generator = self.model.run_algorithm(algo_type)
        self.update_loop()

    def clear_paths(self):
        self.algo_generator = None
        self.model.clear_search_state()
        self.renderer.render(self.model)

    def update_loop(self):
        if self.algo_generator:
            try:
                next(self.algo_generator)
                self.renderer.render(self.model)
                self.root.after(10, self.update_loop)
            except StopIteration:
                self.algo_generator = None
                self.renderer.render(self.model)

    def run(self):
        self.root.mainloop()
