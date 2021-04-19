class State:

    # TODO: Immutable making
    def __init__(self, robot: tuple, butters=[]):
        self.robot = robot
        self.butters = butters

    def __eq__(self, other):
        return self.butters == other.butters and self.robot == other.robot

    def __str__(self):
        return 'Robot at: ' + str(self.robot) + ' Butters at: ' + str(self.butters)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def successor(state: 'State', map_array: list[list[str]], w, h) -> list:
        next_states = []
        robot_y, robot_x = state.robot[0], state.robot[1]

        def is_block(y: int, x: int):
            return map_array[y][x].lower() == 'x'

        def try_move_robot(y: int, x: int):
            """ Tries to move robot and push butters and saves new state in next_states array. """

            # Checking diagonal movement
            if x * y != 0:
                raise Exception('Diagonal moving is not allowed.')

            # Checking bounds
            if robot_x + x >= w or robot_x + x < 0 or robot_y + y >= h or robot_y + y < 0:
                return

            # Checking blocks
            if is_block(robot_y + y, robot_x + x):
                return

            # Checking if there is a butter around
            if (robot_y + y, robot_x + x) not in state.butters:  # There is no butters around
                next_states.append((
                    State((robot_y + y, robot_x + x), state.butters.copy()),
                    (y, x)
                ))
            else:  # There is a butter around
                # Butter not on bound condition
                if (y == -1 and robot_y != 1) or (y == 1 and robot_y != h - 2) or \
                        (x == -1 and robot_x != 1) or (x == 1 and robot_y != w - 2):

                    # if there is block behind butter
                    if is_block(robot_y + 2 * y, robot_x + 2 * x):
                        return

                    # Moving butter
                    new_butters = state.butters.copy()
                    new_butters.remove((robot_y + y, robot_x + x))
                    new_butters.append((robot_y + 2 * y, robot_x + 2 * x))
                    next_states.append((
                        State((robot_y + y, robot_x + x), new_butters),
                        (y, x)
                    ))

        try_move_robot(1, 0)
        try_move_robot(-1, 0)
        try_move_robot(0, 1)
        try_move_robot(0, -1)

        return next_states

    @staticmethod
    def is_goal(state: 'State', points: list[tuple]):
        for butter in state.butters:
            if butter not in points:
                return False
        return True



