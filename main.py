from state import State
from constants import Consts


w, h = 0, 0
map_array = []           # The map array


def parse_map() -> (list, State):
    """ Reads the map file which is addressed in MAP_FILE variable. """
    global w, h
    butters = []        # List of butters on map
    points = []         # List of goal points on map
    robot = (0, 0)      # Robot position

    with open(Consts.MAP_FILE, 'r') as map_file:
        # Reading map width and height
        w, h = [int(x) for x in map_file.readline().split()]
        # Reading map content
        j = 0
        for row in map_file:
            parts = row.split()
            for i, item in enumerate(parts):
                # If found something on block
                if len(item) > 1:
                    if item[1] == 'b':
                        butters.append((j, i))
                    elif item[1] == 'p':
                        points.append((j, i))
                    elif item[1] == 'r':
                        robot = (j, i)
                    # Removing object from map
                    parts[i] = item[0]
            map_array.append(parts)
            j += 1
    return points, State(robot, butters)


def successor(state: State) -> list:
    next_states = []
    robot_y, robot_x = state.robot[0], state.robot[1]

    def try_move_robot(y: int, x: int):
        """ Moves robot without considering bounds. """

        # Checking diagonal movement
        if x * y != 0:
            raise Exception('Diagonal moving is not allowed.')

        # Checking bounds
        if robot_x + x >= w or robot_x + x < 0 or robot_y + y >= h or robot_y + y < 0:
            return

        # Checking if there is a butter around
        if (robot_y + y, robot_x + x) not in state.butters:             # There is no butters around
            next_states.append(
                State((robot_y + y, robot_x + x), state.butters.copy())
            )
        else:                                                           # There is a butter around
            # Butter not on bound condition
            if (y == -1 and robot_y != 1) or (y == 1 and robot_y != h - 2) or\
                    (x == -1 and robot_x != 1) or (x == 1 and robot_y != w - 2):
                new_butters = state.butters.copy()
                new_butters.remove((robot_y + y, robot_x + x))  # Moving butter
                new_butters.append((robot_y + 2 * y, robot_x + 2 * x))
                next_states.append(
                    State((robot_y + y, robot_x + x), new_butters)
                )

    try_move_robot(1, 0)
    try_move_robot(-1, 0)
    try_move_robot(0, 1)
    try_move_robot(0, -1)

    return next_states


def ids_search(init_state: State):
    pass


def __main__():
    points, init_state = parse_map()
    print(init_state)
    for row in successor(init_state):
        print(row)


__main__()
