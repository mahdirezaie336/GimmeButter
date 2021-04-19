from state import State


class Node:

    children: list['Node']

    def __init__(self, state: State, action: tuple, depth: int, parent: 'Node', path_cost, children=[]):
        self.state = state
        self.parent = parent
        self.children = children
        self.book_keeping = [action,            # Action performed on parent
                             depth,             # Depth of this node
                             path_cost,         # Cost from root to here
                             False              # Expanded?
                             ]

    def expand(self, actions: list[tuple[State, tuple, int]]) -> list['Node']:
        children = []
        for action in actions:
            cost = self.book_keeping[2] + action[3]
            depth = self.book_keeping[1] + 1
            parent = self
            new_node = Node(action[0], action[1], depth, parent, cost)
            children.append(new_node)

        self.book_keeping[3] = True
        self.children.extend(children)
        return children

    def equals_int_state(self, other: 'Node'):
        return other.state == self.state

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'State: ' + str(self.state) + ' | ' + str(self.book_keeping)
