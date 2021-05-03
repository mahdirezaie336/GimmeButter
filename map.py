class Map:

    map_array: list[list[str]]
    points: list[tuple[int, int]]

    def __init__(self, h: int, w: int, map_array=[]):
        self.map = map_array
        self.w = w
        self.h = h
        self.points = []

    def set_points(self, points):
        self.points = points

    def get_item(self, y, x) -> str:
        return self.map[y][x]

    def append_row(self, row: list[str]) -> None:
        if len(row) != self.width:
            raise ValueError('Invalid size of columns in this row:\n', str(row))
        Map.map.append(row)
