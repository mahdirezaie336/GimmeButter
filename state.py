from map import Map


class State:

    # TODO: Immutable making
    def __init__(self, robot: tuple, butters=[]):
        self.robot = robot
        self.butters = butters

    def __eq__(self, other):
        return self.butters == other.butters and self.robot == other.robot

    def __str__(self):
        return '"Robot at: ' + str(self.robot) + ' Butters at: ' + str(self.butters) + '"'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        h = hash(self.robot)
        for i in self.butters:
            h += hash(i)
        return h

    @staticmethod
    def successor(state: 'State', map_object: Map, reverse=False) -> list[tuple['State', tuple, int]]:
        map_array = map_object.map
        points = map_object.points
        w, h = map_object.w, map_object.h
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
            if map_object.check_out_of_bounds(robot_y + y, robot_x + x):
                return

            # Checking blocks
            if is_block(robot_y + y, robot_x + x):
                return

            # Checking if there is a butter around
            check_pushing_butter = (robot_y + y, robot_x + x) not in state.butters
            check_pulling_butter = (robot_y - y, robot_x - x) not in state.butters
            if not reverse and check_pushing_butter or reverse and check_pulling_butter:  # There is no butters around
                next_states.append((
                    State((robot_y + y, robot_x + x), state.butters.copy()),
                    (y, x),
                    max(int(map_array[robot_y + y][robot_x + x]), int(map_array[robot_y][robot_x]))
                ))
            else:  # There is a butter around
                # Butter not on bound condition
                if not reverse and ((y == -1 and robot_y != 1) or (y == 1 and robot_y != h - 2) or
                                    (x == -1 and robot_x != 1) or (x == 1 and robot_x != w - 2)) or reverse:

                    # If butter is on a point
                    if not reverse and (robot_y + y, robot_x + x) in points:
                        return

                    # if there is block or another butter behind the butter
                    r2y, r2x = robot_y + 2 * y, robot_x + 2 * x
                    if not reverse and (is_block(r2y, r2x) or ((r2y, r2x) in state.butters)):
                        return

                    # Moving butter
                    new_butters = state.butters.copy()
                    if not reverse:
                        new_butters.remove((robot_y + y, robot_x + x))
                        new_butters.append((r2y, r2x))
                    else:
                        new_butters.remove((robot_y - y, robot_x - x))
                        new_butters.append((robot_y, robot_x))
                    next_states.append((
                        State((robot_y + y, robot_x + x), new_butters),
                        (y, x),
                        max(int(map_array[robot_y + y][robot_x + x]), int(map_array[robot_y][robot_x]))
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
