#Tabakawa's sudoku :3,
import random
import numpy as np
import matplotlib.pyplot as plt

def square_protection(num, j, k, game_matrix, game_size):
    if game_matrix is []:
        return False
    else:
        square = [0,0,0,0]
        j_mod = j % game_size
        k_mod = k % game_size

        square[0] = j - j_mod #min x
        square[1] = k - k_mod #min y
        square[2] = square[0] + game_size-1 #max x
        square[3] = square[1] + game_size-1 #max y


        rest_empty = False
        for row in range(square[0], square[2]+1):
            for column in range(square[1], square[3]+1):
                try:
                    if num == game_matrix[row][column]:

                        return True
                except:
                    rest_empty = True
                    break
            if rest_empty:
                break
        return False

def column_protection(num, column, game_matrix):
    if game_matrix is []:
        return False
    for row in game_matrix:
        if num == row[column]:
            return True
    else:
        return False

def row_protection(num, rowlist):
    if num in rowlist:
        return True
    else:
        return False

def create_game_matrix_solution(game_size):
    x_size = game_size*game_size
    y_size = game_size*game_size
    game_matrix = []
    j = 0
    while j < x_size:
        row = []
        k = 0
        attempt = 0
        while k < y_size:
            exclude_num = [0]
            num = random.choice([l for l in range(1, y_size+1) if l not in exclude_num])

            while row_protection(num,row) or column_protection(num,k,game_matrix) or square_protection(num,j,k,game_matrix,game_size):
                exclude_num.append(num)
                try:
                    num = random.choice([l for l in range(1, y_size+1) if l not in exclude_num])
                except:
                    print(f"RunOutOfExcludedNumbersError: Trying this row again:{j}")
                    k=0
                    attempt = attempt + 1
                    if attempt == (game_size**2) * 2:
                        attempt = 0
                        j = 0
                        game_matrix = []
                    row = []
                    exclude_num = [0]
                    num = random.choice([l for l in range(1, y_size + 1) if l not in exclude_num])

            row.append(num)
            k = k+1

        game_matrix.append(row)
        j = j+1

    return game_matrix

def create_game_matrix(solution_matrix, mode):
    """
    Creates a Sudoku puzzle by randomly removing cells from the solution matrix based on the difficulty mode.
    The removal is done per number (from min to max based on mode), selecting random positions for each number.

    :param solution_matrix: The complete Sudoku solution (list of lists)
    :param mode: Difficulty level ("easy", "medium", "hard")
    :return: The puzzle matrix with some cells set to " "
    """
    size = len(solution_matrix)

    delete_max = 1
    delete_min = 1

    match mode:
        case "easy":
            delete_max = int(np.floor(np.sqrt(size)))
            delete_min = 1
        case "medium":
            delete_max = int(np.floor(np.sqrt(size) * 1.5))
            delete_min = int(np.floor(np.sqrt(size))-1)
        case "hard":
            delete_max = int(np.floor(size - 1))
            delete_min = int(np.floor(np.sqrt(size)))
        case _:
            print("Wrong mode. Going with easy")
            delete_max = int(np.floor(np.sqrt(size)))
            delete_min = 1

    # For each number from delete_min to delete_max
    for num in range(len(solution_matrix) + 1):
        # Find all positions where the number appears
        positions = [(r, c) for r in range(size) for c in range(size) if solution_matrix[r][c] == num]

        # Decide how many to delete for this number (0 to the actual count of occurrences)
        delete_times = random.randint(delete_min, delete_max + 1)

        if delete_times > 0 and positions:
            # Randomly select positions to delete
            to_delete = random.sample(positions, delete_times)
            for r, c in to_delete:
                solution_matrix[r][c] = " "

    return solution_matrix



    return game

def show_game_matrix(game_matrix, gamesize):
    # Převeď na numpy array pro snadnější manipulaci
    np_game_matrix = np.array(game_matrix, dtype=object)
    radky, sloupce = np_game_matrix.shape

    # Vytvoř figuru a osu
    fig, ax = plt.subplots()
    ax.set_xlim(0, sloupce)
    ax.set_ylim(0, radky)
    ax.invert_yaxis()  # Aby řádky šly shora dolů jako v listu

    # Nakresli horizontální čáry (řádky) s tučnými každou x-tou
    for i in range(radky + 1):
        tloustka = 3 if i % gamesize == 0 else 1  # Tučná pro i=0, x, 2x, ...
        ax.axhline(i, lw=tloustka, color='black')

    # Nakresli vertikální čáry (sloupce) s tučnými každou x-tou
    for j in range(sloupce + 1):
        tloustka = 3 if j % gamesize == 0 else 1  # Tučná pro j=0, x, 2x, ...
        ax.axvline(j, lw=tloustka, color='black')

    # Přidej text do středu každé buňky
    for i in range(radky):
        for j in range(sloupce):
            symbol = str(np_game_matrix[i, j]) if np_game_matrix[i, j] != " " else ""  # Mezera se zobrazí prázdná
            ax.text(j + 0.5, i + 0.5, symbol, ha='center', va='center', fontsize=12)

    # Skryj osy
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()


# If run as a file execute: else if added as module it will be skipped
if __name__ == '__main__':
    # Number of squares on each axis (3 would create 9x9 square with squares of 3x3)
    GAME_SIZE = 3
    game_mode = "medium" #easy, medium, hard

    solution = create_game_matrix_solution(GAME_SIZE)
    for i in range(len(solution)):
        print(solution[i])

    print(" ")

    game = create_game_matrix(solution, game_mode)
    for i in range(len(game)):
        print(game[i])

    show_game_matrix(solution, GAME_SIZE)

