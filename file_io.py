class FileIO:

    @staticmethod
    def read_line_by_line(file_name: str) -> list[list[str]]:
        result = []
        with open(file_name, 'r') as map_file:
            for row in map_file:
                result.append(row.split())
        return result
