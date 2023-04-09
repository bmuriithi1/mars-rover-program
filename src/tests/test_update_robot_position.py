from functions.functions import update_robot_position

grid = [ [0,0,0], [0,0,0], [0,0,0]]

def test_zero_old_x_pos_ok():
    old_x_pos = 0
    new_x_pos = 1
    old_y_pos = 1
    new_y_pps = 1
    travel_direction = '>'
    new_grid = [[0, 0, 0], [0, '>', 0], [0, 0, 0]]

    assert update_robot_position(grid, new_x_pos, new_y_pps, travel_direction, old_x_pos, old_y_pos) == new_grid

def test_xpos_at_limit():
    # TODO: Add test once grid size/failure limit is clarified.
    ...