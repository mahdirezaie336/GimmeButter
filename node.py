from state import State


def zero_heuristic(state: State) -> int:
    return 0


class Node:
    children: list['Node']
    action: tuple
    depth: int
    parent: 'Node'
    path_cost: int

    heuristic = zero_heuristic

    def __init__(self, state: State, action=None, depth=0, parent=None, path_cost=0, children=[]):
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

    def equals_int_state(self, other: 'Node') -> bool:
        return other.state == self.state

    def get_identity(self):
        return self.state

    def get_cost(self):
        return self.path_cost + Node.heuristic(self.state)

    def __gt__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
            raise TypeError('Error while comparing object with type', type(other), 'and a Node object')
        return self.get_cost() > other.get_cost()

    def __ge__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
            raise TypeError('Error while comparing object with type', type(other), 'and a Node object')
        return self.get_cost() >= other.get_cost()

    def __lt__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
            raise TypeError('Error while comparing object with type', type(other), 'and a Node object')
        return self.get_cost() < other.get_cost()

    def __le__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
            raise TypeError('Error while comparing object with type', type(other), 'and a Node object')
        return self.get_cost() <= other.get_cost()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'State: ' + str(self.state) + ' | Cost: ' + str(self.get_cost())
