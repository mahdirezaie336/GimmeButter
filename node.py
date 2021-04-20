from state import State


class Node:

    children: list['Node']

    def __init__(self, state: State, action: tuple, depth: int, parent: 'Node', path_cost, children=[]):
        self.state = state
        self.parent = parent
        self.children = children
        self.action = action                # Action performed on parent
        self.depth = depth                  # Depth of this node
        self.path_cost = path_cost          # Cost from root to here
        self.is_expanded = False            # Expanded?

    def expand(self, actions: list[tuple[State, tuple, int]]) -> list['Node']:
        children = []
        for action in actions:
            cost = self.path_cost + action[2]
            depth = self.depth + 1
            parent = self
            new_node = Node(action[0], action[1], depth, parent, cost)
            children.append(new_node)

        self.is_expanded = True
        self.children.extend(children)
        return children

    def equals_int_state(self, other: 'Node'):
        return other.state == self.state

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Action: ' + str(self.action) + ' | Depth' + str(self.depth)
