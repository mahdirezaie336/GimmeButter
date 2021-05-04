from map import Map
from file_io import FileIO
from constants import Consts
from screen_manager import Display
from state import State
from node import Node
import time


class GameManager:
    map: Map
    robot: tuple
    init_state: State

    def __init__(self):
        self.map = None
        self.init_state = None
        self.display = None

        # Reading map file
        self.parse_map()

        # After parsing map it's time to start pygame
        self.display = Display(self.map)

    def parse_map(self):
        map_array = FileIO.read_line_by_line(Consts.MAP_FILE)
        sizes = map_array.pop(0)
        h, w = int(sizes[0]), int(sizes[1])
        self.map = Map(h, w)

        # Variables to read from map
        butters = []
        points = []
        robot = (0, 0)
        for j, row in enumerate(map_array):
            for i, col in enumerate(row):

                # If there is an object in map
                if len(col) > 1:
                    if col[1] == 'b':
                        butters.append((j, i))
                    elif col[1] == 'p':
                        points.append((j, i))
                    elif col[1] == 'r':
                        robot = (j, i)
                    row[i] = col[0]

            # Append row to map
            self.map.append_row(row)

        # Setting map and init state
        self.map.set_points(points)
        self.init_state = State(robot, butters)

    def start_search(self, search_type: str):
        result = self.__getattribute__(search_type + '_search')()

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
        self.display.update(self.init_state)
        self.display.begin_display()

        # Showing way
        if len(result_list) == 0:
            print('There is no way.')
            return
        for state in result_list:
            time.sleep(Consts.STEP_TIME)
            self.display.update(state)

    def ids_search(self) -> Node:
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
                actions = State.successor(node.state, self.map)
                # print(actions)
                visited_states[node.state] = True
                for child in node.expand(actions)[::-1]:

                    if State.is_goal(child.state, self.map.points):
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
            root_node = Node(self.init_state, None, 0, None, 0)
            visited_states = {}
            result = dls_search(i, 0, root_node)
            if result is not None:
                return result
        # If there is no result in IDS
        return None
