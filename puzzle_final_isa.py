import tkinter 
import time
from collections import deque
from heapq import heappop, heappush
from tkinter import *
from tkinter.ttk import *

def Alert_win(err): #window to display alerts
    alert_window = tkinter.Toplevel()
    canvas3 = tkinter.Canvas(alert_window, height=10, width=400)
    alert_window.title("ALERT")
    canvas3.pack()
    #specifying type of alert
    if(err == 1):
        label = Label(alert_window, text="Cannot be Solved")
    elif (err ==2):
        label = Label(alert_window, text="DFS takes a litle while, be patient :)")
    elif(err ==3):
        label = Label(alert_window, text="Input is Not Correct")
    
    label.pack()


def New_Window(algo_choice): #window that shows the puzzle being solved
    global Puz_win
    global canvas2
    
    if(Validate()==True): #checks if input is valid
        Puz_win = tkinter.Toplevel()
        canvas2 = tkinter.Canvas(Puz_win, height=300, width=300)
        Puz_win.title("Puzzle Solution")
        canvas2.pack()
        solved = initialize_puzzle()
        if (solved==1): #checks if puzzle can be solved and algorithim functions being called based on user button press
            if(algo_choice == 1):
                path = bfs(puzzle_state)
            elif(algo_choice == 2):
                #Alert_win(2)
                path = dfs(puzzle_state)
            elif(algo_choice == 3):
                path = a_star(puzzle_state, 1)
            else:
                path = a_star(puzzle_state, 0)
            
            solve_puzzle(path) #calling the fn that solves the puzzle along with the desired algo as parameter
    else:
        Alert_win(3)

    
# main window specifications 
window = tkinter.Tk()
window.title("8x8 Tiles Puzzle")
window.geometry("400x300")

#buttons that offer algorithm options
button = tkinter.Button(window, text="BFS", height= 1, width=5,bg='blue', fg="#FFFFFF", font=(6), command=lambda: New_Window(1))
button.place(x=200, y=190)
button2 = tkinter.Button(window, text="DFS", bg='blue', fg="#FFFFFF", font=(6), height= 1, width=5,  command=lambda: New_Window(2))
button2.place(x=200, y=230)
button3 = tkinter.Button(window, text = "A* M", bg='blue', fg="#FFFFFF", font=(6), height= 1, width=5, command=lambda: New_Window(3))
button3.place(x=265, y=190)
button4 = tkinter.Button(window, text = "A* E", bg='blue', fg="#FFFFFF", font=(6), height= 1, width=5, command=lambda: New_Window(4))
button4.place(x=265, y=230)

def set_text(btn): #sets the textbox value based on keypad press
    widget = window.focus_get()
    print(btn)
    if widget in inputtxt:
        widget.insert("insert", btn)

#setting the keypad
btn_list = [0,1,2,3,4,5,6,7,8]
r = 0
c = 0
buttons =[]
j = 0
for b in btn_list:
    buttons.append(tkinter.Button(window, text=b, width=3 , height=3, bg='light blue', fg="#FFFFFF", font=('bold',16), activebackground='red', activeforeground="#FFFFFF", command=lambda btn=b:set_text(btn)))
    buttons[j].grid(row=r,column=c)
    j+=1
    c += 1
    if c > 2:
        c = 0
        r += 1

# checks if puzzle is solvable by checking number of inversions
def calculate_inversions(state):
    inversions = 0
    flatten_state = [num for row in state for num in row if num != 0]

    for i in range(len(flatten_state)):
        for j in range(i+1, len(flatten_state)):
            if flatten_state[i] > flatten_state[j]:
                inversions += 1

    return inversions


#sets the text fields for the initial state specification
inputtxt =[]
i=0
for row in range(3):
    for col in range(3):
        x = col * 50
        y = row * 50
        inputtxt.append(tkinter.Text(window, width=5, height = 3))
        inputtxt[i].place(x=200+x,y=y)        
        i+=1
tkinter.Label(window, text= "Initial State", font=('bold', 12)).place(x=230, y=160)  
ex_bt = tkinter.Button(window, text='Exit', command=window.destroy)
ex_bt.place(x=150,y=270)


def Validate():
    numcheck = [0] * 9
    for i in range(9):
        if(int(inputtxt[i].get(1.0, "end-1c")) <0 or int(inputtxt[i].get(1.0, "end-1c")) >8):
            return False
        else:
            if(numcheck[int(inputtxt[i].get(1.0, "end-1c"))] != 0 ):
                return False
            else:
                numcheck[int(inputtxt[i].get(1.0, "end-1c"))]=1
    return True

tile_size = 100
puzzle_state = []
puzzle_state_curr = puzzle_state

def initialize_puzzle():
    solved = 1
    global puzzle_state
    puzzle_state = []
    pos = 0
    for row in range(3):
        x = []
        for col in range(3):
            x.append(int(inputtxt[pos].get(1.0, "end-1c")))
            pos+=1
        puzzle_state.append(x)
    # puzzle_state = [[1, 2, 5],
    #                 [3, 4, 0],
    #                 [6, 7, 8]]
    print(puzzle_state)
    if(calculate_inversions(puzzle_state)%2 == 0):
        draw_puzzle(puzzle_state)
    else:
        print("error cant be solved")
        Alert_win(1)
        solved = 0
    return solved

def draw_puzzle(state):
    canvas2.delete("all")
    for row in range(3):
        for col in range(3):
            x = col * tile_size
            y = row * tile_size
            canvas2.create_rectangle(x, y, x+tile_size, y+tile_size, fill="light yellow")
            canvas2.create_text(x + tile_size // 2, y + tile_size // 2, text=state[row][col])
    Puz_win.update()

def update_puzzle_display(state):
    global puzzle_state_curr
    puzzle_state_curr = state
    draw_puzzle(puzzle_state_curr)
    print(state)
def find_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move_tile(state, empty_row, empty_col, new_row, new_col):
    new_state = [row[:] for row in state]
    new_state[empty_row][empty_col] = new_state[new_row][new_col]
    new_state[new_row][new_col] = 0
    return new_state

def generate_successors(state):
    empty_row, empty_col = find_empty_tile(state)
    successors = []

    move_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in move_directions:
        new_row, new_col = empty_row + dr, empty_col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = move_tile(state, empty_row, empty_col, new_row, new_col)
            successors.append(new_state)
    return successors

def calculate_heuristic_euc(state):
    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

    distance = 0

    for row in range(3):
        for col in range(3):
            if state[row][col] != goal_state[row][col] and state[row][col] != 0:
                current_tile = state[row][col]
                goal_row, goal_col = divmod(current_tile - 1, 3)
                distance += ((row - goal_row) ** 2 + (col - goal_col) ** 2) ** 0.5

    return distance



def calculate_heuristic_manhattan(state):
    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

    distance = 0

    for row in range(3):
        for col in range(3):
            if state[row][col] != goal_state[row][col] and state[row][col] != 0:
                distance += abs(state[row][col] // 3 - row) + abs(state[row][col] % 3 - col)

    return distance

def a_star(initial_state, heuristic):
    visited = set()
    if(heuristic == 1):
        heap = [(calculate_heuristic_manhattan(initial_state), 0, initial_state, [])]
    else:
        heap = [(calculate_heuristic_euc(initial_state), 0, initial_state, [])]

    while heap:
        _, cost, state, path = heappop(heap)
        visited.add(str(state))
        
        if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            print("visited:" , visited)
            return path

        successors = generate_successors(state)
        for successor in successors:
            f2 = 0
            if str(successor) not in visited:
                successor_cost = cost + 1
                for i in range(len(heap)):
                    if (heap[i][0] == successor):
                        f2=1
                if (f2 ==0):
                    if(heuristic ==1):
                        heappush(heap, (successor_cost + calculate_heuristic_manhattan(successor), successor_cost, successor, path + [successor]))
                    else:
                        heappush(heap, (successor_cost + calculate_heuristic_euc(successor), successor_cost, successor, path + [successor]))
    
    return None

def bfs(initial_state):
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        visited.add(str(state))
        

        if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            return path

        successors = generate_successors(state)
        for successor in successors:
            if str(successor) not in visited :
                
                queue.append((successor, path + [successor]))

    return None
def dfs(initial_state):
    stack = [(initial_state, [])]
    visited = set()
    

    while stack:
        state, path = stack.pop()
        visited.add(str(state))
        print("visited: ",state)
        
        if state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            return path

        successors = generate_successors(state)
        for successor in successors:
            f1=0
            # if (calculate_inversions(successor) %2==0):
            if str(successor) not in visited :
                    # stack.append((successor, path + [successor]))
                for i in range(len(stack)):
                    if (stack[i][0] == successor):
                        f1=1
                if (f1 ==0):
                    stack.append((successor, path + [successor]))
    return None

def solve_puzzle(path):
    cost=0
    if path is not None:
        for state in path:
            time.sleep(0.5)
            cost+=1
            update_puzzle_display(state)
            
        print("cost:" ,cost)
    else:
        print("No solution found.")




window.mainloop()