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
    # TODO: Reduce code duplication
    next_states = []
    robot_y, robot_x = state.robot[0], state.robot[1]

    # Moving up handling
    if robot_y > 0:
        # Checking if there is a butter upside
        if (robot_y-1, robot_x) not in state.butters:           # There is no butters upside
            next_states.append(
                State((robot_y-1, robot_x), state.butters.copy())
            )
        else:                                                   # There is a butter upside
            # Butter not on bound condition
            if robot_y != 1:
                new_butters = state.butters.copy()
                new_butters.remove((robot_y-1, robot_x))        # Moving butter
                new_butters.append((robot_y-2, robot_x))
                next_states.append(
                    State((robot_y-1, robot_x), new_butters)
                )

    # Moving down handling
    if robot_y < h - 1:
        # Checking if there is a butter downside
        if (robot_y + 1, robot_x) not in state.butters:         # There is no butters downside
            next_states.append(
                State((robot_y + 1, robot_x), state.butters.copy())
            )
        else:                                                   # There is a butter downside
            # Butter not on bound condition
            if robot_y != h - 2:
                new_butters = state.butters.copy()
                new_butters.remove((robot_y + 1, robot_x))      # Moving butter
                new_butters.append((robot_y + 2, robot_x))
                next_states.append(
                    State((robot_y + 1, robot_x), new_butters)
                )

    # Moving right handling
    if robot_x < w - 1:
        # Checking if there is a butter right side
        if (robot_y, robot_x + 1) not in state.butters:         # There is no butters right side
            next_states.append(
                State((robot_y, robot_x + 1), state.butters.copy())
            )
        else:                                                   # There is a butter right side
            # Butter not on bound condition
            if robot_x != w - 2:
                new_butters = state.butters.copy()
                new_butters.remove((robot_y, robot_x + 1))      # Moving butter
                new_butters.append((robot_y, robot_x + 2))
                next_states.append(
                    State((robot_y, robot_x + 1), new_butters)
                )

    # Moving left handling
    if robot_x > 0:
        # Checking if there is a butter left side
        if (robot_y, robot_x - 1) not in state.butters:         # There is no butters left side
            next_states.append(
                State((robot_y, robot_x - 1), state.butters.copy())
            )
        else:                                                   # There is a butter left side
            # Butter not on bound condition
            if robot_x != 1:
                new_butters = state.butters.copy()
                new_butters.remove((robot_y, robot_x - 1))      # Moving butter
                new_butters.append((robot_y, robot_x - 2))
                next_states.append(
                    State((robot_y, robot_x - 1), new_butters)
                )

    return next_states


def ids_search(init_state: State):
    pass


def __main__():
    points, init_state = parse_map()
    print(init_state)
    for row in successor(init_state):
        print(row)


__main__()
