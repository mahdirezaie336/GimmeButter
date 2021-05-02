class Map:

    def __init__(self, map_array: list[list[str]]):
        self.map = map_array

    def get_item(self, y, x) -> str:
        return self.map[y][x]

    def append_row(self, row: list[str]) -> None:
        n = len(row)
        for i in self.map:
            if len(i) != n:
                raise Exception('Size Error: Number of columns is not same as previous rows.')
        Map.map.append(row)
