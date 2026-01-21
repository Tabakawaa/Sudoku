#Tabakawa's sudoku :3,
import random
import numpy as np
import matplotlib.pyplot as plt

# This function returns squares corner locations [top_left,bottom_left,top_right,bottom_right]
def square_detection(row, column, game_size):
    square = [0, 0, 0, 0]
    row_mod = row % game_size
    column_mod = column % game_size

    square[0] = row - row_mod  # min y
    square[1] = column - column_mod  # min x
    square[2] = square[0] + game_size - 1  # max y
    square[3] = square[1] + game_size - 1  # max x

    return square

def square_protection(num, j, k, game_matrix, game_size):
    if game_matrix is []:
        return False
    else:
        square = square_detection(j,k,game_size)


        rest_empty = False
        for row in range(square[0], square[2]+1):
            for column in range(square[1], square[3]+1):
                try:
                    if num == game_matrix[row][column]:
                        #print(f"Square protection is True for {num} at square {square}")
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
            #print(f"Column protection is True for {num} at column {column}")
            return True
    else:
        return False

def row_protection(num, rowlist):
    if num in rowlist:
        #print(f"Row protection is True for {num} at row {rowlist}")
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
                    #print(f"RunOutOfExcludedNumbersError: Trying this row again:{j}")
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

#TODO: Create updated matrix solution generator
def create_game_matrix_solution2(game_size):
    """
    Creates a matrix by creating new square, then tries fitting the square somewhere in matrix.
    If not successful deletes square and tries again.
    :param game_size: number of squares in row or column
    :return:
    """
    size = game_size*game_size
    game_matrix = []

    #Create new empty matrix
    for cell_x in range(size):
        matrix_row = []
        for cell_y in range(size):
            matrix_row.append("x")
        game_matrix.append(matrix_row)
    x = 0
    y = 0
    exclude_num = [0]
    extra_attempts = 0
    master_attempt = 0
    delete_rows_of_squares = 0
    new_square = False
    while game_matrix[size-1][size-1] == "x":
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        print(f"current row {y} is {game_matrix[y]}")
        print(f"and row 0 is {game_matrix[0]}")
        num_not_in_place = True
        if new_square:
            attempts = 0
            extra_attempts = 0
            new_square = False

        num = random.choice([z for z in range(1, size + 1) if z not in exclude_num])
        attempts = 0
        while num_not_in_place:
            square_location = square_detection(y, x, game_size)
            #print(f"I'm inside while num_not_in_place!")

            if not square_protection(num,y,x,game_matrix,game_size) and not row_protection(num,game_matrix[y]) and not column_protection(num,x,game_matrix):
                #print(f"I'm inside if not!")
                num_not_in_place = False
                game_matrix[y][x] = num
                exclude_num.append(num)

                if x == 0 and y == 0:
                    delete_rows_of_squares = 0

                if y == square_location[2] and x == square_location[3]:
                    if square_location[3] == size - 1:
                        y = square_location[2] + 1
                        x = 0
                        exclude_num = [0]
                        new_square = True

                    else:
                        y = square_location[0]
                        x = square_location[3] + 1
                        exclude_num = [0]
                        new_square = True

                # Might seem like a stupid idea, but not exclude_num == [0]
                # actually tells this function if we want to change square or not
                if x == square_location[3] and not exclude_num == [0]:
                    x = square_location[1]
                    y = y + 1
                elif not exclude_num == [0]:
                    x = x + 1
            else:
                # We are not excluding the not suitable number because it could work on another row or column
                #TODO: Add special exclude list for each protection
                num = random.choice([z for z in range(1, size + 1) if z not in exclude_num])
                attempts = attempts + 1
                if attempts > size * size:
                    for i in range(square_location[0], square_location[2] + 1):
                        for j in range(square_location[1], square_location[3] + 1):
                            game_matrix[i][j] = "x"
                            x = square_location[1]
                            y = square_location[0]
                    attempts = 0
                    extra_attempts = extra_attempts + 1

                if extra_attempts > size*np.sqrt(size):
                    #delete entire row of squares
                    #TODO: This should be done for more rows of squares
                    # (I assume something like if in last row delete floor(size/2) - 1 rows?
                    if square_location[0] - game_size * delete_rows_of_squares >= 0:
                        for i in range(square_location[0] - game_size * delete_rows_of_squares, square_location[2] + 1):
                            for j in range(size):
                                game_matrix[i][j] = "x"
                        x = 0
                        y = square_location[0] - game_size * delete_rows_of_squares
                    else:
                        for i in range(square_location[2] + 1):
                            for j in range(size):
                                game_matrix[i][j] = "x"
                        x = 0
                        y = 0

                    extra_attempts = 0
                    master_attempt = master_attempt + 1
                    print(f"Master attempt: {master_attempt}")

                    if master_attempt == 10:
                        delete_rows_of_squares = delete_rows_of_squares + 1
                        master_attempt = 0
                        print(f"Master attempt = 10")
                        print(f"deleting {delete_rows_of_squares} rows of squares")
                exclude_num = [0]

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

#TODO: comment
def show_game_matrix(game_matrix, gamesize):

    np_game_matrix = np.array(game_matrix, dtype=object)
    radky, sloupce = np_game_matrix.shape

    fig, ax = plt.subplots()
    ax.set_xlim(0, sloupce)
    ax.set_ylim(0, radky)
    ax.invert_yaxis()

    for i in range(radky + 1):
        tloustka = 3 if i % gamesize == 0 else 1
        ax.axhline(i, lw=tloustka, color='black')


    for j in range(sloupce + 1):
        tloustka = 3 if j % gamesize == 0 else 1
        ax.axvline(j, lw=tloustka, color='black')


    for i in range(radky):
        for j in range(sloupce):
            symbol = str(np_game_matrix[i, j]) if np_game_matrix[i, j] != " " else ""
            ax.text(j + 0.5, i + 0.5, symbol, ha='center', va='center', fontsize=12)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()


# If run as a file execute: else if added as module it will be skipped
if __name__ == '__main__':
    # Number of squares on each axis (3 would create 9x9 square with squares of 3x3)
    GAME_SIZE = 5
    game_mode = "medium" #easy, medium, hard


    solution = create_game_matrix_solution2(GAME_SIZE)
    show_game_matrix(solution, GAME_SIZE)
    print(solution)


