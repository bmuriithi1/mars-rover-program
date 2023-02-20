# Robot Motion Script

This script takes in instructions of a grid size, initial position of a robot on the grid and commands to move the robot within the grid. 

It outputs the final position of the robot after all commands are executed, or the final known position if the robot has gone off-grid and an indication that the robot has moved off the grid. 

## Inputs and Outputs

Input:
- Grid size: String in format `'4 8'`. 
    - This defines the grid the robot can move in. 
    - I would recommend copying this string inside single quotes, modiyfing the numbers and pasting your modified string when prompted
- Position instructions: String in format `'(2, 3, E) LFRF'`
    - '2' and '3' are respective initial x and y coordinates of robot on grid
    - 'E' is the orientation of the robot. Options for this letter are E (East), W (West), N (North) and S (South)
    - 'LFRFF' is a string with commands to move robot around the string. This string can be of unlimited length - 'LFRFF' is simply an example with 5 commands.
        - F = Move forward one step. 
            - For example, for robot at (0, 0) facing East, the new coordinate would be (0, 1)
            - For example, for robot at (0, 0) facing North, the new coordinate would be (1, 0)
        - L = Rotate left 90 degrees. For example, if facing North, rotate to face West
        - R = Rotate right 90 degrees. For example, if facing North, rotate to face East
    - I would recommend copying the string inside single quotes, modiyfing the numbers and letters and pasting your modified string when prompted
        - Keep the spaces, parentheses and brackets in the same format as the example provided.

Output: 
- If robot stayed within grid, string with final robot position and orientation. eg. `'(3, 4, E)'`
- If robot moved outside the grid, string with final known robot position and 'LOST' string indicating robot is off-grid.`'(3, 4, E) LOST'`
- See example below.
____________________________________________

## Example:

Empty grid using command `'4 8'`: <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>

Initial grid state with robot in place after command `'(2, 3, E) LFRF'`: <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,>,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>

Final state with command `'(2, 3, E) LFRF'`: <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,>] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>
[0,0,0,0] <br>

Output string: `'(3, 4, E)'`

If the robot goes out of the predefined grid, the output string contains the last known position and orientation of the robot, with the string 'LOST' appended to the end of the output. For example, if the input command was `'(2, 3, E) LFRFF'`, the output string would be `'(3, 4, E) LOST'`.
___________

## Executing the program

To execute the program, clone the repository to a folder on your local machine. Navigate to the local repository's root folder and then follow the instructions below depending on whether you want to run the commands via CLI or directly as an executable on Windows.

### Run executable program in Windows

1. From the repository's root directory, navigate to `executable\dist\`
2. Double click executable file `MoveRobotInGrid.exe` to open the Windows Command Prompt
3. Follow instructions in the display or on this README file to provide inputs required to execute program successfully.

### Run executable program via Bash/PowerShell CLI

1. From the repository's root directory, type `.\executable\dist\MoveRobotInGrid.exe` in the command line to execute the program.
2. Follow instructions in the display or on this README file to provide inputs required to execute program successfully.

> CLI commands above based on using PowerShell. Use forward slashes for Linux/Bash terminals.

## TO DO: Future work
- Convert objects to strongly-typed classes for production-level code
    - Class for board, with:
        - properties length, width, x-limit, y-limit
        - instance methods for updating the board after a move
    - Class for robot with:
        - properties defining direction, orientation and possible next moves based on directions
        - instance methods for moving/rotating robot
- Add unit tests to src/tests for thev various functions 
    - use pytest to test functions locally or whilst building program.    
- Improve regex used to parse input:
    - Set realistic limits on grid sizes/max no of commands to prevent program crashing or taking very long to execute
    - Provide help to user by breaking down regex command and detecting what might be missing.
- Improve error handling
    - Use python logging module to print warnings/errors (can set severity using inbuilt lib funcs)
    - Use `try except` statements to gracefully deal with errors, particularly expected ones.
    - For input errors, prompt user to input (up to a limited no of times before exiting program) if input is incorrect first time.
- Add docstrings to all functions describing function, expected inputs and expected outputs
    - See example in `parse_board_details` function
- Clean up comments in code (and action any comments relating to improving functionality)
