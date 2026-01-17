import tkinter as tk
import sudoku
import math


current_matrix = None

def display_matrix(matrix, parent, range_values=(1, 9)):
    if not matrix:
        return

    size = len(matrix)  # Square matrix
    cell_size = 25  # Pixel size of each cell
    y = int(math.sqrt(range_values[1]))  # Block size, e.g., 3 for 9x9 Sudoku

    # Create canvas for the grid
    canvas_width = size * cell_size
    canvas_height = size * cell_size
    grid_canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height, bg="white")
    grid_canvas.pack(pady=20)

    # List of options for dropdown (numbers in range)
    options = [str(i) for i in range(range_values[0], range_values[1] + 1)]
    options.append("Clear")  # Add option to clear the cell

    # Dictionaries for rectangle and text items on canvas (for access)
    rect_dict = {}
    text_dict = {}

    # Set of editable positions (initially empty cells)
    editable = set()

    # Draw cell backgrounds and texts
    for i in range(size):
        for j in range(size):
            cell_value = matrix[i][j]
            symbol = str(cell_value) if cell_value != " " else ""
            is_empty = cell_value == " "

            # Draw background rectangle for each cell
            bg_color = "lightyellow" if is_empty else "white"
            rect_id = grid_canvas.create_rectangle(
                j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size,
                fill=bg_color, outline=""
            )
            rect_dict[(i, j)] = rect_id

            # Draw text
            fg_color = "black"  # Default for initial or empty
            text_id = grid_canvas.create_text(
                (j + 0.5) * cell_size, (i + 0.5) * cell_size,
                text=symbol, font=("Arial", 12), fill=fg_color
            )
            text_dict[(i, j)] = text_id

            if is_empty:
                editable.add((i, j))

    # Draw grid lines with varying thickness
    for i in range(size + 1):
        thickness = 3 if i % y == 0 else 1
        grid_canvas.create_line(0, i * cell_size, canvas_width, i * cell_size, width=thickness, fill="black")

    for j in range(size + 1):
        thickness = 3 if j % y == 0 else 1
        grid_canvas.create_line(j * cell_size, 0, j * cell_size, canvas_height, width=thickness, fill="black")

    # Function to handle value selection from menu
    def select_value(value, i, j):
        if value == "Clear":
            matrix[i][j] = " "
            grid_canvas.itemconfig(text_dict[(i, j)], text="", fill="black")
            grid_canvas.itemconfig(rect_dict[(i, j)], fill="lightyellow")  # Update background to lightyellow
        else:
            matrix[i][j] = int(value)
            grid_canvas.itemconfig(text_dict[(i, j)], text=value, fill="blue")
            grid_canvas.itemconfig(rect_dict[(i, j)], fill="white")  # Update background to white

        # No need to redraw lines since we're updating existing items

    # Bind click on canvas to open menu if editable
    def on_canvas_click(event):
        j = event.x // cell_size
        i = event.y // cell_size
        if (i, j) in editable and 0 <= i < size and 0 <= j < size:
            menu = tk.Menu(parent, tearoff=0)
            for opt in options:
                menu.add_command(label=opt, command=lambda val=opt, ii=i, jj=j: select_value(val, ii, jj))
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    grid_canvas.bind("<Button-1>", on_canvas_click)

def new_game(root, parent,SIZE):
    global current_matrix

    for widget in parent.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()

    current_matrix = sudoku.create_game_matrix(sudoku.create_game_matrix_solution2(SIZE),"hard")
    display_matrix(current_matrix, parent, range_values=(1, SIZE * SIZE))
    window_size = (SIZE ** 2) * 75
    root.geometry(f"{window_size}x{window_size}")


def only_numbers(P):
    return P.isdigit() or P == ""


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sudoku!")
    root.geometry("400x400")

    # Example matrix
    matrix = [
        [1, " ", 2],
        [" ", 3, " "],
        [4, " ", 5]
    ]

    # Display the matrix on start
    display_matrix(matrix, root, range_values=(1, len(matrix)))

    root.mainloop()