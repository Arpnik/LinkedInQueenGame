import numpy as np

class Node:
    def __init__(self, color):
        self.color = color
        self.isQueenPlaced = False

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = np.empty((size, size), dtype=object)
        self.distinctColors = set()

    def addNode(self, row, col, color):
        self.grid[row, col] = Node(color)
        self.distinctColors.add(color)

    def print_grid_structure(self):
        print("Grid Structure:")
        for row in range(self.size):
            for col  in range(self.size):
                cell = self.grid[row,col]
                print(f"Cell ({row }, {col }): "
                      f"Color={cell.color}, "
                        f"Queen={cell.isQueenPlaced}")
