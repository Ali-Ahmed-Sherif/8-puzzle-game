import tkinter as tk
import heapq
import math
import time
import random
import threading
from collections import deque
from tkinter import messagebox

# Define the goal state and possible moves
GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

MOVES = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

# Heuristics
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = divmod(value - 1, 3)
                distance += abs(goal_i - i) + abs(goal_j - j)
    return distance

def euclidean_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = divmod(value - 1, 3)
                distance += math.sqrt((goal_i - i) ** 2 + (goal_j - j) ** 2)
    return distance

# Helper functions
def is_goal(state):
    return state == GOAL_STATE

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move_tile(state, direction):
    blank_i, blank_j = find_blank(state)
    delta_i, delta_j = MOVES[direction]
    new_i, new_j = blank_i + delta_i, blank_j + delta_j

    if 0 <= new_i < 3 and 0 <= new_j < 3:
        new_state = [row[:] for row in state]
        new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
        return new_state
    return None

# Randomly generate a solvable puzzle state
def generate_random_initial_state():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while True:
        random.shuffle(state)
        matrix = [state[:3], state[3:6], state[6:]]
        if is_solvable(matrix):
            return matrix

def is_solvable(matrix):
    state = sum(matrix, [])
    inv_count = sum(
        1 for i in range(len(state)) for j in range(i + 1, len(state))
        if state[i] and state[j] and state[i] > state[j]
    )
    return inv_count % 2 == 0

# Search algorithms with stats tracking
def bfs(initial_state):
    queue = deque([(initial_state, [])])
    visited = set()
    nodes_searched = 0

    while queue:
        current_state, path = queue.popleft()
        nodes_searched += 1
        print(f"Visited node #{nodes_searched}: {current_state}")

        if is_goal(current_state):
            return path, nodes_searched

        visited.add(tuple(tuple(row) for row in current_state))

        for direction in MOVES:
            new_state = move_tile(current_state, direction)
            if new_state and tuple(tuple(row) for row in new_state) not in visited:
                queue.append((new_state, path + [direction]))

    return None, nodes_searched

def dfs(initial_state):
    stack = [(initial_state, [])]  # Stack holds (state, path)
    visited = set()
    nodes_searched = 0

    while stack:
        current_state, path = stack.pop()
        nodes_searched += 1
        print(f"Visited node #{nodes_searched}: {current_state}")

        if is_goal(current_state):
            return path, nodes_searched

        # Mark the state as visited
        visited.add(tuple(tuple(row) for row in current_state))

        # Add new states to the stack in reverse order for consistent DFS behavior
        for direction in reversed(list(MOVES.keys())):
            new_state = move_tile(current_state, direction)
            if new_state and tuple(tuple(row) for row in new_state) not in visited:
                stack.append((new_state, path + [direction]))

    return None, nodes_searched

def a_star(initial_state, heuristic):
    open_set = []
    heapq.heappush(open_set, (heuristic(initial_state), 0, initial_state, []))
    visited = set()
    nodes_searched = 0

    while open_set:
        f_cost, g_cost, current_state, path = heapq.heappop(open_set)
        nodes_searched += 1
        print(f"Visited node #{nodes_searched}: {current_state}")

        if is_goal(current_state):
            return path, nodes_searched

        visited.add(tuple(tuple(row) for row in current_state))

        for direction in MOVES:
            new_state = move_tile(current_state, direction)
            if new_state and tuple(tuple(row) for row in new_state) not in visited:
                new_path = path + [direction]
                new_g_cost = g_cost + 1
                new_f_cost = new_g_cost + heuristic(new_state)
                heapq.heappush(open_set, (new_f_cost, new_g_cost, new_state, new_path))

    return None, nodes_searched

# GUI implementation with tkinter
class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver")
        self.root.configure(bg="#282828")

        # Create a frame for the puzzle board
        self.board_frame = tk.Frame(root, bg="#282828")
        self.board_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Initial state and tiles dictionary
        self.state = generate_random_initial_state()
        self.tiles = {}
        self.entries = [[None] * 3 for _ in range(3)]

        # Draw the initial board
        self.create_board()

        # Input frame
        self.input_frame = tk.Frame(root, bg="#282828")
        self.input_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        for i in range(3):
            for j in range(3):
                entry = tk.Entry(self.input_frame, width=3, font=("Helvetica", 16))
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

        # Buttons for solving and setting initial state
        button_style = {"font": ("Helvetica", 14, "bold"), "bg": "#4CAF50", "fg": "white",
                        "activebackground": "#388E3C"}

        self.bfs_button = tk.Button(root, text="Solve with BFS", command=lambda: self.run_search_thread("BFS"),
                                    **button_style)
        self.bfs_button.grid(row=3, column=0, padx=5, pady=10)

        self.dfs_button = tk.Button(root, text="Solve with DFS", command=lambda: self.run_search_thread("DFS"),
                                    **button_style)
        self.dfs_button.grid(row=3, column=1, padx=5, pady=10)

        self.astar_manhattan_button = tk.Button(root, text="A* (Manhattan)",
                                                command=lambda: self.run_search_thread("A* Manhattan"), **button_style)
        self.astar_manhattan_button.grid(row=3, column=2, padx=5, pady=10)

        self.astar_euclidean_button = tk.Button(root, text="A* (Euclidean)",
                                                command=lambda: self.run_search_thread("A* Euclidean"), **button_style)
        self.astar_euclidean_button.grid(row=3, column=3, padx=5, pady=10)

        # Buttons for setting initial state
        self.random_button = tk.Button(root, text="Random Initial State", command=self.set_random_initial_state,
                                       **button_style)
        self.random_button.grid(row=4, column=0, columnspan=2, pady=10, padx=5)

        self.user_input_button = tk.Button(root, text="Set User Input State", command=self.set_user_initial_state,
                                           **button_style)
        self.user_input_button.grid(row=4, column=2, columnspan=2, pady=10, padx=5)

        # Labels to display runtime, cost, and nodes searched
        label_style = {"font": ("Helvetica", 12), "bg": "#282828", "fg": "white"}
        self.runtime_label = tk.Label(root, text="Runtime: ", **label_style)
        self.runtime_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.cost_label = tk.Label(root, text="Cost (Steps): ", **label_style)
        self.cost_label.grid(row=5, column=2, columnspan=2, pady=10)

        self.nodes_label = tk.Label(root, text="Nodes Searched: ", **label_style)
        self.nodes_label.grid(row=6, column=0, columnspan=4, pady=10)

    def create_board(self):
        """Create or update the board tiles based on the current state."""
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                tile_text = str(value) if value != 0 else ""
                tile_color = "#757575" if value == 0 else "#FFFFFF"

                if (i, j) not in self.tiles:
                    tile = tk.Label(self.board_frame, text=tile_text, font=("Helvetica", 24),
                                    width=4, height=2, bg=tile_color, relief="solid")
                    tile.grid(row=i, column=j, padx=5, pady=5)
                    self.tiles[(i, j)] = tile
                else:
                    self.tiles[(i, j)].config(text=tile_text, bg=tile_color)

    def set_random_initial_state(self):
        """Set a random initial state for the puzzle."""
        self.state = generate_random_initial_state()
        self.create_board()

    def set_user_initial_state(self):
        """Set the puzzle state based on user input in the entries."""
        try:
            state = []
            seen = set()
            for i in range(3):
                row = []
                for j in range(3):
                    value = int(self.entries[i][j].get())
                    if value in seen:
                        messagebox.showerror("Invalid Input", "Duplicates found. Please enter unique values between 0 and 8.")
                        return
                    seen.add(value)
                    row.append(value)
                state.append(row)
            if is_solvable(state):
                self.state = state
                self.create_board()
            else:
                messagebox.showwarning("Unsolvable", "The entered puzzle configuration is not solvable.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers between 0 and 8.")

    def run_search_thread(self, algorithm):
        """Run the selected search algorithm in a separate thread."""
        thread = threading.Thread(target=self.run_search, args=(algorithm,))
        thread.start()

    def run_search(self, algorithm):
        """Run the selected search algorithm and display results."""
        start_time = time.time()
        if algorithm == "BFS":
            path, nodes_searched = bfs(self.state)
        elif algorithm == "DFS":
            path, nodes_searched = dfs(self.state)
        elif algorithm == "A* Manhattan":
            path, nodes_searched = a_star(self.state, manhattan_distance)
        elif algorithm == "A* Euclidean":
            path, nodes_searched = a_star(self.state, euclidean_distance)
        else:
            return

        end_time = time.time()
        runtime = end_time - start_time

        self.runtime_label.config(text=f"Runtime: {runtime:.4f} seconds")
        self.cost_label.config(text=f"Cost (Steps): {len(path) if path else 'N/A'}")
        self.nodes_label.config(text=f"Nodes Searched: {nodes_searched}")

        if path:
            for move in path:
                self.state = move_tile(self.state, move)
                self.create_board()
                time.sleep(0.3)
        else:
            messagebox.showinfo("No Solution", "No solution was found.")

# Run the GUI
root = tk.Tk()
app = PuzzleGUI(root)
root.mainloop()
