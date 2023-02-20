import re
import sys
import time

def main():
    
    print('Initialising robot motion script...')

    # Set count to zero. Use to track amount of movements.
    motion_count = 0
    # Grab input board information
    print()
    
    board_input = input(r"""Input the grid size string (format = '4 8' for 4x8 grid)
    
    Grid size input: """)
    
    rows, cols = parse_board_details(board_input)

    print() # Add newline

    robot_instructions_input = input(r"""Input the position instructions string 
    Format = '(2, 3, E) LFRF' for robot with:
    - intital position of x=2, y=3 
    - Facing East (E) 
    - Commands to sequentially move left, forward, right, forward
    
    Position Instructions: """)

    # Process robot instructions
    robot_instructions = parse_robot_instructions(robot_instructions_input)
    print(str(robot_instructions))

    print() # Add newline

    # Create robot grid and identify x and y limits
    robot_grid_info = create_robot_grid_info(rows, cols)
    x_lim = robot_grid_info["x_lim"]
    y_lim = robot_grid_info["y_lim"]
    print('Printing empty grid and limits')
    print("x_limit: " + str(x_lim) + ', y_limit: ' + str(y_lim))
    print_grid(robot_grid_info["grid"])

    # Check if robot can be placed on board. Print error msg and exit script if false
    x_pos = robot_instructions["x_pos"]
    y_pos = robot_instructions["y_pos"]
    position_check = check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count)

    # Exit program if robot is positioned outside board
    if not position_check:
        return
    
    # Get robot orientation parameters
    orientation_dir = robot_instructions["orientation"]
    orientation_info = get_robot_direction_info(orientation_dir)
    orientation_symbol = orientation_info["direction"]

    # Position robot on board
    update_robot_position(robot_grid_info["grid"], x_pos, y_pos, orientation_symbol)
    print_grid(robot_grid_info["grid"])

    # Execute commands to move robot
    robot_motion_info = robot_instructions["commands"]

    for info in robot_motion_info:
        motion_count += 1
        print (f'Motion count: {motion_count}. Motion is {info}')

        # Move forward command
        if info == 'F':
            # Grab new robot coordinates
            [updated_x_coord, updated_y_coord] = translate_robot(x_pos, y_pos, orientation_symbol)
            
            # Check movement won't take robot off-grid
            position_check = check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count)           
            if not position_check:
                print(f'Last known position: x: {x_pos}, y_pos: {y_pos}')
                print(f'Last known orientation: {orientation_dir}')
                break

            # Update            
            update_robot_position(robot_grid_info["grid"], updated_x_coord, updated_y_coord, orientation_symbol, x_pos, y_pos)
            print(f'Moving forward in {orientation_symbol} direction...')
            print_grid(robot_grid_info["grid"])
            
            x_pos = updated_x_coord
            y_pos = updated_y_coord

        # Rotate robot within grid spot
        elif info == 'L' or info == 'R':
            # Update current orientation direction (N, E, S, W)
            orientation_dir = orientation_info[info]

            # Grab new orientation info (dir symbol, possible future orientations)
            orientation_info = get_robot_direction_info(orientation_dir)

            # Update orientation symbol and update grid
            orientation_symbol = orientation_info['direction']
            print(f'Rotating to {orientation_symbol} direction...')
            update_robot_position(robot_grid_info["grid"], x_pos, y_pos, orientation_symbol)
            print_grid(robot_grid_info["grid"])

        # Deal with unrecognised motion input. Shouldn't be invoked if I parse commands correctly during input
        else:
            exit_message = 'Motion input not recognised, check input.'
            exit_script(exit_message)

        #time.sleep(1)

    # Return output
    lost_string = 'LOST' if position_check == False else ''
    output_string = f"({x_pos}, {y_pos}, {orientation_dir}) {lost_string}"
    print(f"\nFinal robot position: {output_string} \nScript complete. Exiting in 5s")
    time.sleep(5)

    return

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
    # TO DO: Check and limit board size - if someone puts in '1,000,000 1,000,000', it could take a while...
    regex_search = re.search(r"(\d) (\d)", board_input_str)
    if regex_search == None:
        exit_message = f'Regex Error! Check your input string: {board_input_str}'
        exit_script(exit_message)

    board_rows = int(regex_search.group(1))
    board_cols = int(regex_search.group(2))

    return (board_rows, board_cols)

def parse_robot_instructions(instructions_input_str: str) -> dict[str, any]:

    # Look for string
    # TO DO: Maybe limit length of commands - if someone puts in a long list, script could take a while...
    regex_search = re.search(r"\((\d+), (\d+), ([NESW])\)\s([LFR]+)", instructions_input_str)
    
    # TO DO: Be more specific in identifying which part of string (eg. command, init x/y, etc) is missing
    if regex_search == None:
        exit_message = f'Regex Error! Check your input string: {instructions_input_str}'
        exit_script(exit_message)
    
    # TO DO: Convert obj into a strongly-typed class for prod code
    robot_instructions_obj = {
        "x_pos": int(regex_search.group(1)),
        "y_pos": int(regex_search.group(2)),
        "orientation": regex_search.group(3),
        "commands": regex_search.group(4)
    }

    return robot_instructions_obj

# Create grid with possible motion of robot
def create_robot_grid_info(col_no: int, row_no: int) -> dict[str, any]:

    grid = [[0] * col_no for row in range(row_no)]

    # Convert to strongly-typed class for prod
    grid_dict = {"grid": grid, "x_lim": col_no - 1, "y_lim": row_no - 1 }

    return grid_dict

# Display grid
def print_grid(grid: list[list]) -> None:

    for row in grid[::-1]: 
        print(row)

    print('----------------')

    return

# Check robot position is OK. True if robot's x and y coords are below limits
def check_robot_position(
        x_pos: int, 
        y_pos: int, 
        x_lim: int, 
        y_lim: int, 
        motion_count: int
    ) -> bool:
    
    motion_allowed = x_pos < x_lim and y_pos < y_lim
    
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
    if old_x_pos and old_y_pos:
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

if __name__ == "__main__":
    main()