from state import State


class Node:

    def __init__(self, state: State, parent, children=[]):
        self.state = state
        self.parent = parent
        self.children = children

