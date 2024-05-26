import argparse
import os
import run_nuXmv

import board_builder


def create_smv_file(fileName):
    pBoard, keeper_row, keeper_col, num_of_goals, goal_position_col, goal_position_row = board_builder.build_pBoard(
        fileName)
    pBoard_col = len(pBoard[0])
    pBoard_row = len(pBoard)

    output_dir = "SMV_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    fileName = fileName.replace("Input/", "")
    smv_file_name = output_dir + "/" + fileName.rstrip(".txt") + ".smv"
    with open(smv_file_name, "w") as f:
        f.write(f"""MODULE main
VAR
    move : {{u, d, l, r, p_u, p_d, p_l, p_r, 0}};
    keeper_col : 1..{pBoard_col};
    keeper_row : 1..{pBoard_row};
    box_to_row : 0..{pBoard_row};
    box_to_col : 0..{pBoard_col};
    box_from_row : 0..{pBoard_row};
    box_from_col : 0..{pBoard_col};
    pBoard : array 1..{pBoard_row} of array 1..{pBoard_col} of {{"-", "#", ".", "*", "+", "$", "@"}};
ASSIGN
""")
        for i, row in enumerate(pBoard):
            for j, char in enumerate(row):
                f.write(f'    init(pBoard[{i + 1}][{j + 1}]) := "{char}";\n')

        f.write(f""" 
    init(box_to_col) := 0;
    init(box_to_row) := 0;
    init(box_from_col) := 0;
    init(box_from_row) := 0;
    init(keeper_col) := {keeper_col + 1};
    init(keeper_row) := {keeper_row + 1};
    init(move) := r;
""")

        f.write(f""" 
    next(move) := 
    case
        (keeper_row > 2 )&(pBoard[(keeper_row) - 1][keeper_col] = "-" | pBoard[(keeper_row)-1][keeper_col] = ".") : u;
        TRUE : 0;
    esac union
    case
        (keeper_row < {pBoard_row} -1 )&(pBoard[keeper_row+1][keeper_col] = "-" | pBoard[keeper_row+1][keeper_col] = ".") : d;
     TRUE : 0;
    esac union
    case
        (keeper_col > 2 )&(pBoard[keeper_row][(keeper_col)-1] = "-" | pBoard[keeper_row][(keeper_col)-1] = ".") : l;
     TRUE : 0;
    esac union
    case
        (keeper_col < {pBoard_col} -1)&(pBoard[keeper_row][keeper_col+1] = "-" | pBoard[keeper_row][keeper_col+1] = ".") : r;
     TRUE : 0;
    esac union
    case
        (keeper_row > 3)&(pBoard[(keeper_row)-1][keeper_col] = "$" | pBoard[(keeper_row)-1][keeper_col] = "*") & (pBoard[(keeper_row)-2][keeper_col] = "-" | pBoard[(keeper_row)-2][keeper_col] = ".") : p_u;
        TRUE : 0;
    esac union
    case
        (keeper_row < {pBoard_row}-2 )&(pBoard[keeper_row+1][keeper_col] = "$" | pBoard[keeper_row+1][keeper_col] = "*") & (pBoard[keeper_row+2][keeper_col] = "-" | pBoard[keeper_row+2][keeper_col] = ".") : p_d;
        TRUE : 0;
    esac union
    case
        (keeper_col > 3)&(pBoard[keeper_row][(keeper_col)-1] = "$" | pBoard[keeper_row][(keeper_col)-1] = "*") & (pBoard[keeper_row][(keeper_col)-2] = "-" | pBoard[keeper_row][(keeper_col)-2] = ".") : p_l;
        TRUE : 0;
    esac union
    case
        (keeper_col < {pBoard_col}-2 )&(pBoard[keeper_row][keeper_col+1] = "$" | pBoard[keeper_row][keeper_col+1] = "*") & (pBoard[keeper_row][keeper_col+2] = "-" | pBoard[keeper_row][keeper_col+2] = ".") : p_r;
        TRUE : 0;
    esac union 0;

""")

        # next Puzzle Board configuration after a move
        f.write(f"""
    next(box_to_row):= case
        (next(move) = p_u)& (keeper_row > 3): keeper_row -2;
        (next(move) = p_d) & (keeper_row < {pBoard_row - 2}): keeper_row + 2;
        (next(move) = p_r) : keeper_row;
        (next(move) = p_l) : keeper_row;
        TRUE : 0;
    esac;

    next(box_to_col):= case
        (next(move) = p_r)& (keeper_col < {pBoard_col - 2}) : keeper_col + 2;
        (next(move) = p_l)& (keeper_col > 3) : keeper_col - 2;
        (next(move) = p_u) : keeper_col;
        (next(move) = p_d) : keeper_col;
        TRUE : 0;
    esac;

        next(box_from_row):= case
        (next(move) = p_u) & (keeper_row > 1) : keeper_row - 1;
        (next(move) = p_d) & (keeper_row < {pBoard_row - 2}): keeper_row + 1;
        (next(move) = p_r) : keeper_row ;
        (next(move) = p_l) : keeper_row;
        TRUE : 0;
    esac;

    next(box_from_col):= case
        (next(move) = p_r) & (keeper_col < {pBoard_col - 2}): keeper_col + 1;
        (next(move) = p_l) & (keeper_col > 2): keeper_col - 1;
        (next(move) = p_u) : keeper_col;
        (next(move) = p_d) : keeper_col;
        TRUE : 0;
    esac;


    next(keeper_row):= case
        ((next(move) = u) | (next(move) = p_u) ) & (keeper_row > 2): keeper_row - 1;
        ((next(move) = d) | (next(move) = p_d) ) & (keeper_row < {pBoard_row - 1}) : keeper_row + 1;
        TRUE : keeper_row;
    esac;

    next(keeper_col):= case
        ((next(move) = l) | (next(move) = p_l)) & (keeper_col > 1 ) : keeper_col - 1;
        ((next(move) = r) | (next(move) = p_r) )& (keeper_col < {pBoard_col - 1} ) : keeper_col + 1;
        TRUE : keeper_col;
    esac;
""")

        #         for i in range(pBoard_row):
        #             for j in range(pBoard_col):
        #                 # Cells that are wall are not changing
        #                 if(pBoard[i][j] == "#"):
        #                     f.write(f"""
        #     next(pBoard[{i+1}][{j+1}]) := pBoard[{i+1}][{j+1}];\n""")
        #         #next Puzzle Board configuration after a move
        #         f.write(f"""
        #     next(goals_position_col[1]):= case
        #         TRUE: goals_position_col[1];
        #     esac;

        #     next(goals_position_row[1]):= case
        #         TRUE: goals_position_row[1];
        #     esac;
        # """)

        # Update cells on the board
        for i in range(pBoard_row):
            for j in range(pBoard_col):
                # Cells that are wall are not changing
                if (pBoard[i][j] == "#"):
                    f.write(f"""  
    next(pBoard[{i + 1}][{j + 1}]) := pBoard[{i + 1}][{j + 1}];\n""")
                # Update the non-wall cells
                if (pBoard[i][j] != "#"):
                    f.write(f"""
    next(pBoard[{i + 1}][{j + 1}]):= case
        (pBoard[{i + 1}][{j + 1}] = "+")& (next(move) !=0 ) : ".";
        (pBoard[{i + 1}][{j + 1}] = "@")& (next(move) !=0 ) : "-";
        (pBoard[{i + 1}][{j + 1}] = "-" | pBoard[{i + 1}][{j + 1}] = "$") & next(keeper_row)={i + 1} & next(keeper_col)={j + 1} : "@";
        (pBoard[{i + 1}][{j + 1}] = "." | pBoard[{i + 1}][{j + 1}] = "*") & next(keeper_row)={i + 1} & next(keeper_col)={j + 1} : "+";
        (pBoard[{i + 1}][{j + 1}] = "-") & next(box_to_row={i + 1}) &  next(box_to_col={j + 1}) : "$";
        (pBoard[{i + 1}][{j + 1}] = ".") & next(box_to_row={i + 1}) &  next(box_to_col={j + 1}) : "*";
        (pBoard[{i + 1}][{j + 1}] = "$") & next(box_from_row={i + 1}) &  next(box_from_col={j + 1}) : "-";
        (pBoard[{i + 1}][{j + 1}] = "*") & next(box_from_row={i + 1}) &  next(box_from_col={j + 1}) : ".";
        TRUE : pBoard[{i + 1}][{j + 1}];
        esac;

        """)

        f.write("\nDEFINE\n")

        for i in range(num_of_goals):
            f.write(f'    goals_position_col[{i + 1}] := {goal_position_col[i]};\n')
        for i in range(num_of_goals):
            f.write(f'    goals_position_row[{i + 1}] := {goal_position_row[i]};\n')

        goal_conditions = []
        for i in range(num_of_goals):
            goal_conditions.append(f"(pBoard[goals_position_row[{i + 1}]][goals_position_col[{i + 1}]] = \"*\")")

        goal = " & ".join(goal_conditions)

        f.write(f"""
    LTLSPEC !((move!=0) U ({goal}));    
        """)
    print(f"pBoard initialization written to smv_file.smv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('fileName', type=str, help='The input filename')
    #parser.add_argument('solver_engine', type=str, help='The solver engine')
    args = parser.parse_args()

    fileName = "Input/"+args.fileName

    create_smv_file(fileName)
    smv_fileName = "SMV_files/"+fileName.replace("Input/", "").replace(".txt", ".smv")
    run_nuXmv.run_nuxmv_interactive(smv_fileName)
