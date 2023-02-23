# 
# Functions used in the Mars Rover Program
#

import re
import sys
import time

def get_board_input():
    board_input_str = input(r"""Input the grid size string (format = '4 8' for 4x8 grid)
    
    Grid size input: """)

    return board_input_str

def get_position_instructions():
    position_input_str = input(r"""Input the position instructions string 
    Format = '(2, 3, E) LFRF' for robot with:
    - intital position of x=2, y=3 
    - Facing East (E) 
    - Commands to sequentially move left, forward, right, forward
    
    Position Instructions: """)

    return position_input_str

def parse_board_details(board_input_str: str) -> tuple[int, int]:

    """
    Function to parse input board size (string) and return a the number of rows/columns the board has.
    If input string is in invalid format, the script will not be executed.

    Inputs
    -----------------
    board_input_str (str):  String containing the rows and columns.

    Outputs
    -----------------
    (board_rows, board_cols) (tuple):   Tuple with the no. of rows and columns the board, assuming input is valid.

    """

    # Grab board details and raise error if regex pattern isn't found. Could prompt user to input again.
    # TODO: Check and limit board size if using nested lists. If someone puts in '1,000,000 1,000,000', it could take a while.
    regex_search = re.search(r"(\d) (\d)", board_input_str)
    if regex_search == None:
        exit_message = f'Regex Error! Check your input string: {board_input_str}'
        exit_script(exit_message)

    board_rows = int(regex_search.group(1))
    board_cols = int(regex_search.group(2))

    return (board_rows, board_cols)

def parse_robot_instructions(instructions_input_str: str) -> dict[str, any]:

    # Look for string
    # TODO: Maybe limit length of commands - if someone puts in a long list, script could take a while.
    regex_search = re.search(r"\((\d+), (\d+), ([NESW])\)\s([LFR]+)", instructions_input_str)
    
    # TODO: Be more specific in identifying which part of string (eg. command, init x/y, etc) is missing
    if regex_search == None:
        exit_message = f'Regex Error! Check your input string: {instructions_input_str}'
        exit_script(exit_message)
    
    # TODO: Convert obj into a strongly-typed class for prod code
    robot_instructions_obj = {
        "x_pos": int(regex_search.group(1)),
        "y_pos": int(regex_search.group(2)),
        "orientation": regex_search.group(3),
        "commands": regex_search.group(4)
    }

    return robot_instructions_obj

# Create grid with possible motion of robot
def create_robot_grid_info(col_no: int, row_no: int) -> dict[str, any]:
    
    # TODO: Review data type. Use nested dictionary instead for reduced memory
    grid = [[0] * col_no for row in range(row_no)]

    # TODO: Convert to strongly-typed class for prod
    # TODO: Clarify requirements - grid limits and instructions seem incompatible?
    grid_dict = {"grid": grid, "x_lim": col_no - 1, "y_lim": row_no -1 }

    return grid_dict

# Display grid
def print_grid(grid: list[list]) -> None:

    for row in grid[::-1]: 
        print(row)

    print('----------------')

    return None

# Check robot position is OK. True if robot's x and y coords are below limits
def check_robot_position(
        x_pos: int, 
        y_pos: int, 
        x_lim: int, 
        y_lim: int, 
        motion_count: int
    ) -> bool:
    
    motion_allowed = x_pos <= x_lim and y_pos <= y_lim and x_pos >= 0 and y_pos >= 0
    
    if not motion_allowed and motion_count < 1:
        print('Robot is outside grid! Place it inside grid')
    
    elif not motion_allowed:
        print('Robot has moved out of bounds!')
        
    return motion_allowed

# Add/update robot location and reset old position to zero.
def update_robot_position(
        grid: list[list], 
        new_x_pos: int, 
        new_y_pos: int, 
        travel_direction: str = 'X', 
        old_x_pos: any = None, 
        old_y_pos: any = None
    ) -> list[list]:
    
    grid[new_y_pos][new_x_pos] = travel_direction
    if type(old_x_pos) == int and type(old_y_pos) == int:
        grid[old_y_pos][old_x_pos] = 0

    return grid

# Get information about robot's current and possible future rotation directions
def get_robot_direction_info (current_orientation: str) -> dict[str, str]:
    
    # 'L' = left direction, 'R' - right direction
    orientation_dict = {
        'E': { 'direction': '>',
            'L': 'N',  
            'R': 'S' 
        },
        'W': { 'direction': '<',
            'L': 'S', 
            'R': 'N'
        },
        'N': { 'direction': '^', 
            'L': 'W',
            'R': 'E'
        },
        'S': { 'direction': 'V', 
            'L': 'E', 
            'R': 'W'
        }
    }

    robot_direction_info = orientation_dict[current_orientation]
    
    return robot_direction_info

# Move forward and update coordinates
def translate_robot(x_coord: int, y_coord: int, translation_dir: str) -> list[int, int]:
    translation_dict = {
        '>': x_coord + 1,
        'V': y_coord - 1,
        '<': x_coord - 1,
        '^': y_coord + 1
    }
    if translation_dir in '<>':
        new_x_coord = translation_dict[translation_dir]
        new_y_coord = y_coord
    elif translation_dir in 'V^':
        new_x_coord = x_coord
        new_y_coord = translation_dict[translation_dir]
    else: 
        exit_msg = 'Translation direction not known! Check input.'
        exit_script(exit_msg)
    
    return [new_x_coord, new_y_coord]

def exit_script(exit_msg): 
    print(exit_msg + '\n\nExiting script in 5s...')
    time.sleep(5)
    sys.exit()