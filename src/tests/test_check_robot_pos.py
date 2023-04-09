from functions.functions import check_robot_position

def test_west_limit_failure():
    x_pos=-1 
    y_pos=0 
    x_lim=4
    y_lim=8
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == False

def test_west_limit_ok():
    x_pos=0
    y_pos=0
    x_lim=4
    y_lim=8
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == True

def test_south_limit_failure():
    x_pos=1
    y_pos=-1
    x_lim=4
    y_lim=8
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == False

def test_south_limit_ok():
    x_pos=1
    y_pos=0
    x_lim=4
    y_lim=8
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == True

def test_east_limit_failure():
    x_pos=5
    y_pos=1
    x_lim=4
    y_lim=8
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == False

def test_east_limit_ok():
    x_pos=4
    y_pos=1
    x_lim=4
    y_lim=8
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == True

def test_north_limit_failure():
    x_pos=1
    y_pos=5
    x_lim=4
    y_lim=4
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == False

def test_north_limit_ok():
    x_pos=1
    y_pos=4
    x_lim=4
    y_lim=4
    motion_count=5
    assert check_robot_position(x_pos, y_pos, x_lim, y_lim, motion_count) == True
