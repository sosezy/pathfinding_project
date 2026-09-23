import heapq
import random
import math

class GridModel:
    def __init__(self, rows=55, cols=70):
        self.rows = rows
        self.cols = cols
        self.generate_random_grid()

    def generate_random_grid(self, obstacle_prob=0.25):
        self.grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (2, 2)
        self.end = (self.rows - 3, self.cols - 3)
        
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < obstacle_prob:
                    self.grid[r][c] = '#'
        
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.end[0]][self.end[1]] = 'E'
        self.clear_search_state()

    def load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            lines = [line.strip().split() for line in f if line.strip()]
        if not lines: return
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.grid = lines
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S': self.start = (r, c)
                elif self.grid[r][c] == 'E': self.end = (r, c)
        self.clear_search_state()

    def clear_search_state(self):
        self.visited = set()
        self.frontier = set()
        self.came_from = {}
        self.current_node = None
        self.final_path = []
        self.is_finished = False

    def get_neighbors(self, r, c):
        # 8 направлений для диагонального движения как на видео
        neighbors = []
        dirs = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

    def heuristic(self, a, b, algo_type):
        if algo_type == "Dijkstra": return 0
        return math.hypot(a[0] - b[0], a[1] - b[1]) # Евклидово расстояние

    def get_current_path(self):
        # Реконструкция пути от текущей проверяемой точки (эффект дрожания)
        if self.is_finished:
            return self.final_path
        if not self.current_node:
            return []
        
        path = []
        curr = self.current_node
        while curr in self.came_from:
            path.append(curr)
            curr = self.came_from[curr]
        path.append(self.start)
        return path[::-1]

    def run_algorithm(self, algo_type="A*"):
        self.clear_search_state()
        count = 0
        open_set = []
        heapq.heappush(open_set, (0, count, self.start))
        self.came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end, algo_type)}
        open_set_hash = {self.start}

        iterations = 0
        while open_set:
            current = heapq.heappop(open_set)[2]
            open_set_hash.remove(current)
            self.current_node = current

            if current == self.end:
                self.final_path = self.get_current_path()
                self.is_finished = True
                yield True
                return

            self.visited.add(current)
            if current in self.frontier:
                self.frontier.remove(current)

            for neighbor in self.get_neighbors(current[0], current[1]):
                temp_g_score = g_score[current] + (1.414 if neighbor[0] != current[0] and neighbor[1] != current[1] else 1)
                
                if temp_g_score < g_score.get(neighbor, float('inf')):
                    self.came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, self.end, algo_type)
                    if neighbor not in open_set_hash:
                        count += 1
                        heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        self.frontier.add(neighbor)
            
            iterations += 1
            if iterations % 2 == 0: # Сдаем управление UI каждые 2 шага для плавности
                yield False
