from state import State
from constants import Consts
from node import Node
from screen_manager import Display


w, h = 0, 0
map_array = []              # The map array
points = []                 # List of goal points on map


def parse_map() -> State:
    """ Reads the map file which is addressed in MAP_FILE variable. """
    global w, h
    butters = []        # List of butters on map
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

    return State(robot, butters)


def ids_search(init_state: State):

    # Implementing DLS to be used in IDS
    def dls_search(k: int) -> Node:
        """ This DLS implementation is used in IDS search.
            :param k Maximum depth
            :returns Node of goal if Goal state is found"""

        frontier = []                   # Frontier stack for searching
        visited_states = {}             # Visited states list
        root_node = Node(init_state, None, 0, None, 0)

        # Beginning non-recursive DLS
        frontier.append(root_node)
        while len(frontier) > 0:
            last = frontier.pop()
            actions = State.successor(last.state, map_array, w, h)
            if State.is_goal(last.state, points):
                return last

            visited_states[last.state] = True
            for child in last.expand(actions):
                if child.depth < k and not visited_states.get(child.state, False):
                    frontier.append(child)
                if len(frontier) > 50:
                    raise Exception('Frontier overflow')
        # If there is no result in DLS
        return None

    # IDS Implementation
    for i in (Consts.FIRST_K, Consts.LAST_K):
        result = dls_search(i)
        if result is not None:
            return result
    # If there is no result in IDS
    return None


def __main__():
    # Initializing map and pygame
    init_state = parse_map()
    display = Display(map_array, w, h, points)

    # Finding way
    result = ids_search(init_state)
    print(result.state)

    display.begin_display()


__main__()
