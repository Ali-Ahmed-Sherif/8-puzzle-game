# 8-puzzle-game
8 puzzle game using BFS, DFS, and A*
8-Puzzle Solver Report
Introduction
The 8-puzzle is a classic sliding puzzle where the goal is to arrange tiles in ascending order, leaving the blank tile (0) in the bottom-right corner. This report documents the algorithms used to solve this puzzle (BFS, DFS, and A*), their performance, and a comparison based on several metrics: path cost, nodes expanded, search depth, and running time. The objective is to solve the puzzle efficiently while gathering insights on each algorithm's behavior and performance in reaching the goal state.

1. Problem Setup
•	Goal State: The configuration [[1, 2, 3], [4, 5, 6], [7, 8, 0]].
•	Initial State: Randomly generated and solvable configuration of the puzzle.
•	Actions: Moving the blank tile (0) up, down, left, or right.
2. Algorithms and Data Structures

2.1 Breadth-First Search (BFS)
•	Description: BFS explores all nodes at the current depth level before moving on to nodes at the next depth level. It's guaranteed to find the shortest path in terms of the number of moves if a solution exists.
•	Data Structure Used: Queue (collections.deque) for managing nodes in a first-in, first-out manner.
•	Implementation Highlights:
o	Nodes are dequeued, and their successors are enqueued.
o	Visited states are tracked using a set to avoid revisiting nodes.

2.2 Depth-First Search (DFS)
•	Description: DFS explores nodes by going as deep as possible along each branch before backtracking. Although DFS is not optimal for this problem, it can find a solution quickly if the goal is deep in the search tree.
•	Data Structure Used: Stack (list) for managing nodes in a last-in, first-out manner.
•	Implementation Highlights:
o	Nodes are added to the stack in reverse order to maintain consistent DFS behavior.
o	Like BFS, DFS tracks visited states to prevent infinite loops.

2.3 A Search (A with Manhattan and Euclidean heuristics)**
•	Description: A* uses a priority queue to select the node with the lowest estimated total cost (f = g + h) at each step. The two heuristics used are:
o	Manhattan Distance: The sum of the absolute differences between current and goal positions of each tile.
o	Euclidean Distance: The straight-line (Euclidean) distance from each tile’s current position to its goal position.
•	Data Structure Used: Min-Heap (using heapq) as a priority queue to efficiently fetch the node with the lowest f-cost.
•	Implementation Highlights:
o	heapq.heappush() and heapq.heappop() manage the priority queue.
o	Nodes store both their cumulative cost (g_cost) and their heuristic estimate to goal (h_cost).



3. Assumptions
. We created a method that detects odd inversions in the random state or input state from the user so an alert will pop on the screen emphasizing and warning the user that such state is unsolvable.
 

. We initiated 2 different ways of triggering an initial state either by:
-"""Set a random initial state for the puzzle."""
"""Set the puzzle state based on user input in the entries."""

Moreover, any sort of errors that may occur from the user side got handled to avoid program freezing or collapsing
 
•		The running time measurement excludes time for GUI updates to focus purely on algorithm performance.



4. Metrics for Comparison
•	Path to Goal: The sequence of moves (up, down, left, right) from the initial to goal state.
•	Cost of Path: The number of moves required to reach the goal (solution depth).
•	Nodes Expanded: Total nodes visited during the search process.
•	Search Depth: The depth level at which the solution was found.
•	Running Time: Execution time from start to completion for each algorithm.

5. Extra Work
•	GUI for Visualization: Developed an eye catchy Tkinter GUI that allows users to visualize the puzzle state and solution steps.
 
•	Heuristic Comparison: Added Euclidean heuristic to compare with Manhattan, demonstrating the impact of heuristic choice on A* performance.
•	Multi-threading for Real-Time Interaction: Implemented search algorithms in separate threads to prevent GUI freezing.
•	 
•	Handling errors and exceptions
•	Manifesting critical information regarding the solution including: Runtime, Cost, steps, Nodes searched, and visualizing the movement of tiles.


