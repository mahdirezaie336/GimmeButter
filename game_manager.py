from map import Map
from file_io import FileIO
from constants import Consts
from screen_manager import Display
from state import State
from node import Node
from heap_hashtable import MinHeap
import time


class GameManager:

    map: Map
    init_state: State
    display: Display

    def __init__(self):
        self.map, self.init_state = self.parse_map()
        # After parsing map it's time to start pygame
        self.display = Display(self.map)

    def start_search(self, search_type: str) -> list[State]:
        """ Chooses a search between all and returns its result list.
            :param search_type Search algorithm type
            :returns The result of search"""

        result = self.__getattribute__(search_type + '_search')()

        # Putting path to goal in list
        if search_type in ['bd_bfs', 'reverse_bfs']:
            return result
        else:
            result_list = GameManager.extract_path_list(result)
            result_list.reverse()
            return result_list

    def display_states(self, states_list: list[State]) -> None:
        """ Gets a list of states and displays it into display object.
            :param states_list List of states to show """

        if len(states_list) <= 0:
            print('There is no way')
            return

        self.display.update(self.init_state)                            # Starting display
        self.display.begin_display()

        for state in states_list:
            time.sleep(Consts.STEP_TIME)
            self.display.update(state)

    def bd_bfs_search(self) -> list[Node]:
        """ Performs a bidirectional BFS from initial state to all goal states.
            :returns List of states to reach from init to goal"""

        def bd_bfs(init: State, goal: State) -> (Node, Node):           # Bidirectional BFS for two nodes
            """ Performs a bidirectional BFS from a state to a specific goal state.
                :param init The initial state
                :param goal The specific goal state
                :returns Two nodes in which the two searches meet together. """

            init_node = Node(init)
            goad_node = Node(goal)
            frontier1 = [Node(init)]
            frontier2 = [Node(goal)]
            visited1 = {init: init_node}
            visited2 = {goal: goad_node}

            while len(frontier1) > 0 and len(frontier2) > 0:            # Starting BFS loop
                node_1 = frontier1.pop(0)

                node_2 = frontier2.pop(0)

                if node_2.state in visited1:                            # If we reach from initial state to goal
                    return visited1[node_2.state], node_2

                if node_1.state in visited2:                            # If we reach from goal to initial state
                    return node_1, visited2[node_1.state]

                # TODO: Move successor and predecessor calling into node expand function
                actions = State.successor(node_1.state, self.map)       # Add successors to frontier
                for child in node_1.expand(actions):
                    if child.state not in visited1:
                        frontier1.append(child)
                        visited1[child.state] = child

                actions = State.predecessor(node_2.state, self.map)     # Add predecessors to frontier
                for child in node_2.expand(actions):
                    if child.state not in visited2:
                        frontier2.append(child)
                        visited2[child.state] = child

            return None, None

        #########################################################################
        # Here we find all possible goal node and do bidirectional bfs two by two
        #########################################################################

        new_butters = self.init_state.butters.copy()                # Putting Butters into points to create goal state
        for i, point in enumerate(self.map.points):
            new_butters[i] = point

        all_goal_states = []                            # Putting the robot in all possible positions around butter
        for i, point in enumerate(self.map.points):
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_y = point[0] + direction[0]
                new_x = point[1] + direction[1]

                # Checking out of bounds or blocks
                if self.map.check_out_of_bounds(new_y, new_x) or self.map.is_block(new_y, new_x):
                    continue

                # Checking butters around butter
                if (new_y, new_x) in new_butters:
                    continue

                state = State((new_y, new_x), new_butters.copy())
                all_goal_states.append(state)

        shortest_list = []                                                  # Do Bidirectional BFS two by two
        shortest_length = float('inf')
        print('Found', len(all_goal_states), 'possible ways.')
        for goal_state in all_goal_states:
            node1, node2 = bd_bfs(self.init_state, goal_state)
            if node1 is None or node2 is None:
                continue

            result_list = GameManager.extract_path_list(node1)              # Converting nodes to list
            result_list.reverse()
            result_list.pop()
            result_list.pop(0)
            result_list.extend(GameManager.extract_path_list(node2))
            if len(result_list) < shortest_length:                          # Setting the minimum
                print('Found a way with', len(result_list), 'moves.')
                shortest_length = len(result_list)
                shortest_list = result_list

        return shortest_list

    def ids_search(self) -> Node:
        """ Performs an iterative deepening search from initial state to goal.
            :returns The node which contains goal state"""

        def dls_search(limit: int, depth: int, node: Node) -> Node:         # Implementation of DLS to be used in IDS
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

                    r = dls_search(limit, depth + 1, child)         # Recursive calling
                    if r is not None:
                        res = r
                        break

                    # To avoid adding non-visited states into visited states list
                    if child.state in visited_states:
                        del visited_states[child.state]

            return res

        for i in range(Consts.FIRST_K, Consts.LAST_K):              # IDS Implementation
            print('Starting with depth', i)
            cur_time = time.time()
            root_node = Node(self.init_state)
            visited_states = {}
            result = dls_search(i, 0, root_node)
            if result is not None:
                return result

    def a_star_search(self) -> Node:
        """ Performs an A* search from initial state to goal state.
            :returns The node containing the goal state."""

        def euclid_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:
            """ Finds euclid distance between two points. """
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

        def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
            """ Finds manhattan distance between to points. """
            d1 = point1[0] - point2[0]
            d2 = point1[1] - point2[1]
            if d1 < 0:
                d1 *= -1
            if d2 < 0:
                d2 *= -1
            return d1 + d2

        def heuristic(state: State) -> int:
            """ The heuristic function which evaluates steps from a state to goal.
                :param state The state to evaluate."""

            # Finding closest butter
            closest_butter = state.butters[0]
            min_d_to_butter = float('inf')
            for butter in state.butters:
                d = euclid_distance(butter, state.robot)
                if d < min_d_to_butter:
                    min_d_to_butter = d
                    closest_butter = butter

            # Finding closest point to butter
            min_d_to_point = float('inf')
            for point in self.map.points:
                d = euclid_distance(point, closest_butter)
                if d < min_d_to_point:
                    min_d_to_point = d

            return int(min_d_to_point + min_d_to_butter)

        Node.heuristic = heuristic                                          # Setting all nodes heuristic functions

        heap = MinHeap()                                                    # Beginning of a star search
        root_node = Node(self.init_state)
        heap.add(root_node)
        while not heap.is_empty():
            node = heap.pop()

            time.sleep(0.5)
            self.display.update(node.state)
            print(node.path_cost + heuristic(node.state))

            # Checking goal state
            if State.is_goal(node.state, self.map.points):
                return node

            # A* search
            actions = State.successor(node.state, self.map)
            for child in node.expand(actions):
                heap.add(child)

    def reverse_bfs_search(self) -> list[State]:

        def reverse_bfs(goal: State):

            frontier = [Node(goal)]
            visited = {goal: True}

            while len(frontier) > 0:  # Starting BFS loop
                node = frontier.pop(0)

                if node.state == self.init_state:
                    return node

                actions = State.predecessor(node.state, self.map)  # Add successors to frontier
                for child in node.expand(actions):
                    if child.state not in visited:
                        frontier.append(child)
                        visited[child.state] = True

        new_butters = self.init_state.butters.copy()  # Putting Butters into points to create goal state
        for i, point in enumerate(self.map.points):
            new_butters[i] = point

        all_goal_states = []  # Putting the robot in all possible positions around butter
        for i, point in enumerate(self.map.points):
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_y = point[0] + direction[0]
                new_x = point[1] + direction[1]

                # Checking out of bounds or blocks
                if self.map.check_out_of_bounds(new_y, new_x) or self.map.is_block(new_y, new_x):
                    continue

                # Checking butters around butter
                if (new_y, new_x) in new_butters:
                    continue

                state = State((new_y, new_x), new_butters.copy())
                all_goal_states.append(state)

        shortest_list = []  # Do Bidirectional BFS two by two
        shortest_length = float('inf')
        all_goal_states.reverse()
        for goal_state in all_goal_states:

            node1 = reverse_bfs(goal_state)
            if node1 is None:
                continue

            result_list = GameManager.extract_path_list(node1)  # Converting nodes to list
            if len(result_list) < shortest_length:  # Setting the minimum
                print(len(result_list))
                shortest_length = len(result_list)
                shortest_list = result_list

        return shortest_list

    def bfs_search(self) -> Node:

        frontier = [Node(self.init_state)]
        visited = {}

        while len(frontier) > 0:  # Starting BFS loop
            node_1 = frontier.pop(0)
            visited[node_1.state] = node_1

            if State.is_goal(node_1.state, self.map.points):
                return node_1

            actions = State.successor(node_1.state, self.map)  # Add successors to frontier
            for child in node_1.expand(actions):
                if child.state not in visited:
                    frontier.append(child)

    @staticmethod
    def parse_map() -> (Map, State):
        """ Uses map file to create map object in game.
            :returns The map object and the init state"""

        map_array = FileIO.read_line_by_line(Consts.MAP_FILE)
        sizes = map_array.pop(0)
        h, w = int(sizes[0]), int(sizes[1])
        map_object = Map(h, w)

        butters = []                                            # Variables to read from map
        points = []
        robot = (0, 0)
        for j, row in enumerate(map_array):
            for i, col in enumerate(row):

                if len(col) > 1:                                # If there is an object in map
                    if col[1] == 'b':
                        butters.append((j, i))
                    elif col[1] == 'p':
                        points.append((j, i))
                    elif col[1] == 'r':
                        robot = (j, i)
                    row[i] = col[0]

            map_object.append_row(row)                          # Append row to map

        map_object.set_points(points)
        return map_object, State(robot, butters)

    @staticmethod
    def extract_path_list(node: Node) -> list[State]:
        """ Gets a node and returns a list of states which contains all states from root to the node.
            :param node The node to get its path
            :returns The list of all states from root to the node"""

        result_list = []
        watchdog = 0
        while node is not None:
            watchdog += 1
            if watchdog > 1000:
                raise Exception('Watchdog limit exceeded')
            result_list.append(node.state)
            node = node.parent

        return result_list

    @staticmethod
    def state_in_list_of_nodes(state: State, nodes_list: list[Node]) -> bool:
        for node in nodes_list:
            if node.state == state:
                return True
        return False
