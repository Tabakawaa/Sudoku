import app
import sudoku
import tkinter as tk

# Main window
root = tk.Tk()
root.title("Sudoku!")

# Game size 3 -> 9x9
SIZE = 3
window_size = (SIZE ** 2) * 50

root.geometry(f"{int(window_size*4/3)}x{int(window_size*3/4)}")
mainframe = tk.Frame(root)
mainframe.pack(fill="both", expand=True)


v_cmd = (root.register(app.only_numbers), "%P")

size_field_entry = tk.Entry(root, validate="key", validatecommand=v_cmd)
size_field_entry.pack(padx=5, pady=5, side="top")

new_button = tk.Button(root, text="New sudoku", command=lambda:app.new_game(root, mainframe,int(size_field_entry.get())))
new_button.pack(padx=5, pady=5, side="top")

root.mainloop()