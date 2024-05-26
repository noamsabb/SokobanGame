
#get_board_dimensions
def get_board_dimensions(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        rows = len(lines)
        cols = max(len(line.strip()) for line in lines)
    return rows, cols

#Check if the character is valid
def isValid(char):
    valid_chars = {'#', '-', '.', '$', '@'}  # Set of valid characters
    return char in valid_chars

#Build pBoard
def build_pBoard(fileName):
    num_of_goals = 0
    goal_col = []
    goal_row = []
    try:
        rows, cols = get_board_dimensions(fileName)

        # Initialize pBoard with the appropriate dimensions
        pBoard = [['' for _ in range(cols)] for _ in range(rows)]


        with open(fileName, 'r') as file:
            for row_index, line in enumerate(file):
                line = line.strip()
                for col_index, char in enumerate(line):
                    if isValid(char):
                        pBoard[row_index][col_index] = char
                        if(char == '@'):
                            keeper_row = row_index
                            keeper_col = col_index
                        if(char == '.'):
                            num_of_goals += 1
                            goal_col.append(col_index+1)
                            goal_row.append(row_index+1)
                    else:
                        raise ValueError(
                            f"Invalid character '{char}' in the file at row {row_index + 1}, column {col_index + 1}.")
    except Exception as e:
        print(f"Something went Wrong: {e}")
        return None

    return pBoard, keeper_row, keeper_col,num_of_goals,goal_col,goal_row

# if __name__ == "__main__":
#     fileName = "example.txt"
#     pBoard, keeper_row, keeper_col,num_of_goals,goal_col,goal_row = build_pBoard(fileName)
#     if pBoard is not None:
#         for row in pBoard:
#             print(''.join(row))
#
#     print(goal_col)
#
#     print(goal_row)

