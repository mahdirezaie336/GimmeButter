from state import State
from constants import Consts
from node import Node
from screen_manager import Display
import time

w, h = 0, 0
map_array = []  # The map array
points = []  # List of goal points on map
display = None


def parse_map() -> State:
    """ Reads the map file which is addressed in MAP_FILE variable.
        :returns The initial state"""
    global w, h
    butters = []  # List of butters on map
    robot = (0, 0)  # Robot position

    with open(Consts.MAP_FILE, 'r') as map_file:
        # Reading map width and height
        h, w = [int(x) for x in map_file.readline().split()]
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


def ids_search(init_state: State) -> Node:
    # Implementing DLS to be used in IDS
    def dls_search(limit: int, depth: int, node: Node) -> Node:
        """ This DLS implementation is used in IDS search.
            :param limit: Maximum depth
            :param depth: The explored depth until now
            :param node: The node the expand next
            :returns Node of goal if Goal state is found"""

        if time.time() - cur_time > 30.0:
            raise Exception('Time limit exceeded')

        # display.update(node.state)
        # time.sleep(0.08)

        res = None
        if depth < limit and node.state not in visited_states:
            actions = State.successor(node.state, map_array, w, h, points)
            # print(actions)
            visited_states[node.state] = True
            for child in node.expand(actions)[::-1]:

                if State.is_goal(child.state, points):
                    return child

                # Recursive calling
                r = dls_search(limit, depth + 1, child)
                if r is not None:
                    res = r
                    break

                # To avoid adding non-visited states into visited states list
                if child.state in visited_states:
                    del visited_states[child.state]

        return res

    # IDS Implementation
    for i in range(Consts.FIRST_K, Consts.LAST_K):
        print('Starting with depth', i)
        cur_time = time.time()
        root_node = Node(init_state, None, 0, None, 0)
        visited_states = {}
        result = dls_search(i, 0, root_node)
        if result is not None:
            return result
    # If there is no result in IDS
    return None


def __main__():
    global display
    # Initializing map and pygame
    init_state = parse_map()
    # print(State.successor(init_state, map_array, w, h))
    display = Display(map_array, w, h, points)

    # Finding way
    result = ids_search(init_state)

    # Putting path to goal in list
    result_list = []
    watchdog = 0
    while result is not None:
        watchdog += 1
        if watchdog > 1000:
            raise Exception('Watchdog limit exceeded')
        result_list.append(result.state)
        result = result.parent
    result_list.reverse()

    # Starting display
    display.update(init_state)
    display.begin_display()

    # Showing way
    if len(result_list) == 0:
        print('There is no way.')
        return
    for state in result_list:
        time.sleep(Consts.STEP_TIME)
        display.update(state)


__main__()
