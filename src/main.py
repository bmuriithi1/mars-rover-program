import time
import functions.functions as function

def main():
    
    print('Initialising robot motion script...')

    # Set count to zero. Use to track amount of movements.
    motion_count = 0
    # Grab input board information
    print()
    board_input = function.get_board_input()
    
    rows, cols = function.parse_board_details(board_input)

    print() # Add newline
    robot_instructions_input = function.get_position_instructions()

    # Process robot instructions
    robot_instructions = function.parse_robot_instructions(robot_instructions_input)
    print(str(robot_instructions))

    print() # Add newline

    # Create robot grid and identify x and y limits
    robot_grid_info = function.create_robot_grid_info(rows, cols)
    x_lim = robot_grid_info["x_lim"]
    y_lim = robot_grid_info["y_lim"]
    print('Printing empty grid and limits')
    print("x_limit: " + str(x_lim) + ', y_limit: ' + str(y_lim))
    function.print_grid(robot_grid_info["grid"])

    # Check if robot can be placed on board. Print error msg and exit script if false
    x_pos = robot_instructions["x_pos"]
    y_pos = robot_instructions["y_pos"]
    position_check = function.check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count)

    # Exit program if robot is positioned outside board
    if not position_check:
        return
    
    # Get robot orientation parameters
    orientation_dir = robot_instructions["orientation"]
    orientation_info = function.get_robot_direction_info(orientation_dir)
    orientation_symbol = orientation_info["direction"]

    # Position robot on board
    function.update_robot_position(robot_grid_info["grid"], x_pos, y_pos, orientation_symbol)
    function.print_grid(robot_grid_info["grid"])

    # Execute commands to move robot
    robot_motion_info = robot_instructions["commands"]

    for info in robot_motion_info:
        motion_count += 1
        print (f'Motion count: {motion_count}. Motion is {info}')

        # Move forward command
        if info == 'F':
            # Grab new robot coordinates
            [updated_x_coord, updated_y_coord] = function.translate_robot(x_pos, y_pos, orientation_symbol)
            
            # Check movement won't take robot off-grid
            position_check = function.check_robot_position(updated_x_coord, updated_y_coord, x_lim, y_lim, motion_count)           
            if not position_check:
                print(f'Last known position: x: {x_pos}, y_pos: {y_pos}')
                print(f'Last known orientation: {orientation_dir}')
                break

            # Update            
            function.update_robot_position(robot_grid_info["grid"], updated_x_coord, updated_y_coord, orientation_symbol, x_pos, y_pos)
            print(f'Moving forward in {orientation_symbol} direction...')
            function.print_grid(robot_grid_info["grid"])
            
            x_pos = updated_x_coord
            y_pos = updated_y_coord

        # Rotate robot within grid spot
        elif info == 'L' or info == 'R':
            # Update current orientation direction (N, E, S, W)
            orientation_dir = orientation_info[info]

            # Grab new orientation info (dir symbol, possible future orientations)
            orientation_info = function.get_robot_direction_info(orientation_dir)

            # Update orientation symbol and update grid
            orientation_symbol = orientation_info['direction']
            print(f'Rotating to {orientation_symbol} direction...')
            function.update_robot_position(robot_grid_info["grid"], x_pos, y_pos, orientation_symbol)
            function.print_grid(robot_grid_info["grid"])

        # Deal with unrecognised motion input. Shouldn't be invoked if I parse commands correctly during input
        else:
            exit_message = 'Motion input not recognised, check input.'
            function.exit_script(exit_message)

        #time.sleep(1)

    # Return output
    lost_string = 'LOST' if position_check == False else ''
    output_string = f"({x_pos}, {y_pos}, {orientation_dir}) {lost_string}"
    print(f"\nFinal robot position: {output_string} \nScript complete. Exiting in 5s")
    time.sleep(5)

    return None

if __name__ == "__main__":
    main()