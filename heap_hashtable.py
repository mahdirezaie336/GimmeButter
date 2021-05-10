class MinHeap:

    def __init__(self, array=[], index_table={}):
        self.array = array
        self.index_table = index_table
        self.make_heap()

    def make_heap(self):
        for i in range(len(self.array) // 2).__reversed__():
            self.min_heapify(i)
        for index, vertex in enumerate(self.array):
            self.index_table[vertex.get_identity()] = index

    def add(self, vertex):
        index = len(self.array)
        self.array.append(vertex)
        self.index_table[vertex.get_identity()] = index
        self.min_up_heapify(index)

    def remove(self, vertex_id=None, index=None):
        if index is None:
            index = self.index_table[vertex_id]
        last_item = self.array[-1]
        self.index_table[last_item.get_identity()] = index
        self.array[index] = last_item

        del self.index_table[vertex_id]
        del self.array[-1]

        if len(self.array) != 0:
            self.min_heapify(index)
            self.min_up_heapify(index)

    def modify(self, vertex_id, new_value):
        index = self.index_table[vertex_id]
        self.array[index].value = new_value
        self.min_up_heapify(index)
        self.min_heapify(index)

    def pop(self):
        root = self.array[0]
        self.remove(self.array[0].get_identity(), 0)
        return root

    def is_empty(self):
        return len(self.array) == 0

    def value_of(self, vertex_id):
        return self.array[self.index_table[vertex_id]]

    def get_vertex(self, vertex_id):
        index = self.index_table[vertex_id]
        return self.array[index]

    def min_heapify(self, i):
        # Makes a heap when the item with index i has a right and left
        # subtrees which both are heaps.
        le = self.left(i)
        ri = self.right(i)
        smallest = self.minimum(le, ri, i)
        if smallest != i:
            self.swap(i, smallest)
            self.min_heapify(smallest)

    def min_up_heapify(self, i):
        pa = self.parent(i)
        smallest = self.minimum(pa, i)
        if smallest != pa:
            self.swap(pa, i)
            self.min_up_heapify(pa)

    def right(self, i):
        ri = 2 * i + 2
        if ri < len(self.array):
            return ri
        return i

    def left(self, i):
        ri = 2 * i + 1
        if ri < len(self.array):
            return ri
        return i

    def parent(self, i):
        pa = (i - 1) // 2
        if pa < 0:
            return 0
        return pa

    def swap(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp

        self.index_table[self.array[i].get_identity()] = i
        self.index_table[self.array[j].get_identity()] = j

    def minimum(self, *index):
        smallest = index[0]
        for i in index:
            if self.array[i] < self.array[smallest]:
                smallest = i
        return smallest

    def __str__(self):
        return str(self.array)

    def __contains__(self, vertex_id):
        return vertex_id in self.index_table

    def print(self):
        for i in self.array:
            print(i)
        print(self.index_table)
        print()
