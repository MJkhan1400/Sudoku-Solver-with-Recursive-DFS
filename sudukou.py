import tkinter as tk
import random
import math

def get_board_from_string(board):
    num_rows = int(math.sqrt(len(board)))
    num_cols = num_rows
    # Creating an empty 2D list
    board_list = [[] for _ in range(num_rows)]
    
    for row in range(num_rows):
        # Extract digits for this row and add to list
        row_string = board[(row*num_cols):(row*num_cols)+num_cols]
        board_list[row] = [int(num) for num in row_string]
    
    return board_list

def generate_sudoku_board():
    # Initializing an empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    # Generating a random completed Sudoku board
    fill_board(board)
    # Removing some numbers randomly to create a puzzle
    remove_numbers(board, 45)  # Adjust the second parameter to control difficulty
    return board

def fill_board(board):
    # Initializing a list containing numbers 1 to 9 in random order
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    # Recursiving function to fill the board
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for num in numbers:
        if valid(board, num, (row, col)):
            board[row][col] = num

            if fill_board(board):
                return True

            board[row][col] = 0

    return False

def valid(board, num, pos):
    # Checking row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Checking column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Checking box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

def remove_numbers(board, num_to_remove):
    # Removing numbers randomly while keeping the solution unique
    cells = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(cells)
    for cell in cells:
        row, col = cell
        temp = board[row][col]
        board[row][col] = 0
        temp_board = [row[:] for row in board]
        if not solve_board(temp_board):
            board[row][col] = temp
        num_to_remove -= 1
        if num_to_remove == 0:
            break

def solve_board(board):
    # This is the recursive DFS function to solve the board
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve_board(board):
                return True

            board[row][col] = 0

    return False

class SudokuSolver():
    def __init__(self, board):
        self.board = board

    def find_next_empty(self, empty_val: int=0):
        num_rows = len(self.board)
        num_cols = len(self.board[0])
        
        for row in range(num_rows):
            for col in range(num_cols):
                if self.board[row][col] == empty_val:
                    return (row, col)
                
        return None

    def is_valid_number(self, board, number, position):
        
        # Here we will assign the board dimensions to variables.
        num_rows = len(board)
        square_size = int(math.sqrt(num_rows))
        
        row_idx, col_idx = position
        
        # Checking if number is already present in current row
        if number in board[row_idx]:
            return False
        
        # Checking if number is already present in current column
        current_column_values = [board[row][col_idx] for row in range(num_rows)]
        if number in current_column_values:
            return False
        
        # Geting indices of the 3x3 square that our position lies in
        square_x_idx = col_idx // square_size
        square_y_idx = row_idx // square_size
        # Check if number is already present in current 3x3 square
        for row in range(square_y_idx * square_size, (square_y_idx * square_size) + square_size):
            for col in range(square_x_idx * square_size, (square_x_idx * square_size) + square_size):
                if board[row][col] == number and (row, col) != position:
                    return False
        
        # And If we reach this point we can say the number is valid
        return True

    def solve(self):
        # Determineing that no more empty squares are left and then finishing
        next_empty_pos = self.find_next_empty()

        if not next_empty_pos:
            # Here we are determing that the board is full and the puzzle is solved
            return True
        else:
            row, col = next_empty_pos

        # here we are trying every number at the current empty position
        for i in range(1, 10):
            # Checking if number is valid in this position or not
            if self.is_valid_number(board=self.board, number=i, position=(row, col)):
                # Put the number in the board
                self.board[row][col] = i
                # Now we continue solving with the updated board by calling solve function again
                if self.solve():
                    # Here we determine that no more empty positions - solution found
                    return True

        # We are at a dead end and need to backtrack.
        # So we will set the current cell value to 0 and continue execution of the previous call to solve.
        self.board[row][col] = 0
        return False

    def print_board(self):
        num_rows = len(self.board)
        num_cols = len(self.board[0])
        square_size = int(math.sqrt(num_rows))

        # Printing one row at a time
        for row in range(num_rows):
            # Inserting characters to define grid lines
            if row != 0 and row % square_size == 0:
                print("- " * (num_cols + square_size - 1))

            # Printing numbers at each column
            for col in range(num_cols):
                # Insert characters to define grid lines
                if col != 0 and col % square_size == 0:
                    print("| ", end="")

                # Printing numbers - only include newline at last column
                number = self.board[row][col]
                if col < num_cols-1:
                    print(f"{number} ", end="")
                else:
                    print(number)

# Here we are designing the GUI
class SudokuGUI:
    def __init__(self, master, solver):
        self.master = master
        self.solver = solver
        self.create_widgets()

    def create_widgets(self):
        self.master.configure(bg='#00001A')

        container = tk.Frame(self.master, bg='#00001A')
        container.pack()

        title = tk.Label(container, text="DFS Sudoku Solver", font=("Arial", 48), fg="wheat", bg='#00001A')
        title.pack(pady=40)
        subtitle = tk.Label(container, text="This programme uses recursive depth first search algorithm\nto solve the randomly generated sudoku boards.\n\nMade by Mohammad Jazib Khan", font=("Arial", 12), fg="wheat", bg='#00001A')
        subtitle.pack(pady=10)

        board_frame = tk.Frame(container, bg="wheat", bd=10, relief="solid", borderwidth=10, padx=10, pady=10, highlightbackground="wheat", highlightcolor="wheat", highlightthickness=10)
        board_frame.pack(pady=40)

        self.cells = [[None for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                cell_bg = "white" if (i // 3 + j // 3) % 2 == 0 else "light grey"
                if i % 3 == 0 and j % 3 == 0:
                    borderwidth = 5
                else:
                    borderwidth = 2
                self.cells[i][j] = tk.Entry(board_frame, width=2, font=('Arial', 24), justify='center', bg=cell_bg, bd=0, highlightthickness=0, borderwidth=borderwidth)
                self.cells[i][j].grid(row=i, column=j, padx=3, pady=3)

        button_container = tk.Frame(container, bg='#00001A')
        button_container.pack()

        generate_button = tk.Button(button_container, text="Generate", font=("Arial", 28), bg="wheat", bd=0, padx=20, pady=10, command=self.generate_sudoku)
        generate_button.pack(side=tk.LEFT, padx=10)

        solve_button = tk.Button(button_container, text="Solve", font=("Arial", 28), bg="wheat", bd=0, padx=20, pady=10, command=self.solve_sudoku)
        solve_button.pack(side=tk.LEFT, padx=10)

        generate_button.bind("<Enter>", lambda event, btn=generate_button: self.on_enter(event, btn))
        generate_button.bind("<Leave>", lambda event, btn=generate_button: self.on_leave(event, btn))
        solve_button.bind("<Enter>", lambda event, btn=solve_button: self.on_enter(event, btn))
        solve_button.bind("<Leave>", lambda event, btn=solve_button: self.on_leave(event, btn))



    def on_enter(self, event, btn):
        btn.config(bg="#c4a769", fg="white")

    def on_leave(self, event, btn):
        btn.config(bg="wheat", fg="black")

    def generate_sudoku(self):
        random_board = generate_sudoku_board()
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if random_board[i][j] != 0:
                    self.cells[i][j].insert(0, str(random_board[i][j]))

    def solve_sudoku(self):
        board = [[0 for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                entry_text = self.cells[i][j].get()
                if entry_text:
                    board[i][j] = int(entry_text)

        self.solver.board = board
        self.solver.solve()

        solved_board = self.solver.board

        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].insert(0, str(solved_board[i][j]))

# This is the main fucntion to stat the application
def main():
    root = tk.Tk()
    root.title("Sudoku Solver with Recursive DFS")
    root.geometry("1080x1080")

    solver = SudokuSolver([])
    SudokuGUI(root, solver)
    root.mainloop()

if __name__ == "__main__":
    main()

