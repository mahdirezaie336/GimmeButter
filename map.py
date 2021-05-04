class Map:

    map_array: list[list[str]]
    points: list[tuple[int, int]]

    def __init__(self, h: int, w: int, map_array=[]):
        self.map = map_array
        self.w = w
        self.h = h
        self.points = []

    def check_out_of_bounds(self, y: int, x: int) -> bool:
        return x >= self.w or x < 0 or y >= self.h or y < 0

    def is_block(self, y: int, x: int):
        return self.map[y][x].lower() == 'x'

    def set_points(self, points):
        self.points = points

    def get_item(self, y, x) -> str:
        return self.map[y][x]

    def append_row(self, row: list[str]) -> None:
        if len(row) != self.w:
            raise ValueError('Invalid size of columns in this row:\n', str(row))
        self.map.append(row)
