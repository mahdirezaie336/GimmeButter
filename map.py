class Map:

    def __init__(self, map_array: list[list[str]], h: int, w: int):
        self.map = map_array
        self.width = w
        self.height = h

    def get_item(self, y, x) -> str:
        return self.map[y][x]

    def append_row(self, row: list[str]) -> None:
        if len(row) != self.width:
            raise ValueError('Invalid size of columns in this row:\n', str(row))
        Map.map.append(row)
