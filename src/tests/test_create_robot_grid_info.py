from functions.functions import create_robot_grid_info

# TODO - update limits once clarified.
def test_robot_grid_pos_xlim():  
    grid_dict = create_robot_grid_info(4, 8)
    assert grid_dict["x_lim"] == 3

# TODO - update limits once clarified.
def test_robot_grid_pos_ylim():
    grid_dict = create_robot_grid_info(4, 8)  
    assert grid_dict["y_lim"] == 7