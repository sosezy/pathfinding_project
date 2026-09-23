import heapq

class GridModel:
    def __init__(self, rows=30, cols=30):
        self.rows = rows
        self.cols = cols
        self.reset_grid()

    def reset_grid(self):
        self.grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)
        self.grid[self.start[0]][self.start[1]] = 'S'
        self.grid[self.end[0]][self.end[1]] = 'E'
        self.clear_search_state()

    def clear_search_state(self):
        self.visited = set()
        self.frontier = set()
        self.path = []
        self.is_finished = False

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

    def get_neighbors(self, r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

    def heuristic(self, a, b, algo_type):
        if algo_type == "Dijkstra": return 0
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # A* Manhattan

    def run_algorithm(self, algo_type="A*"):
        self.clear_search_state()
        count = 0
        open_set = []
        heapq.heappush(open_set, (0, count, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end, algo_type)}
        
        open_set_hash = {self.start}

        while open_set:
            current = heapq.heappop(open_set)[2]
            open_set_hash.remove(current)

            if current == self.end:
                curr = self.end
                while curr in came_from:
                    self.path.append(curr)
                    curr = came_from[curr]
                self.path.append(self.start)
                self.path.reverse()
                self.is_finished = True
                yield True
                return

            self.visited.add(current)
            if current in self.frontier:
                self.frontier.remove(current)

            for neighbor in self.get_neighbors(current[0], current[1]):
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, self.end, algo_type)
                    if neighbor not in open_set_hash:
                        count += 1
                        heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        self.frontier.add(neighbor)
            yield False
