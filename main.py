from state import State
from constants import Consts


w, h = 0, 0


def parse_map() -> (list, list, State):
    """ Reads the map file which is addressed in MAP_FILE variable. """
    global w, h
    map_list = []       # The map array
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
            map_list.append(parts)
            j += 1
    return map_list, points, State(robot, butters)


def __main__():

    pass
