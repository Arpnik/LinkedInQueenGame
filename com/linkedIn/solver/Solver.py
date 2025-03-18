class Solver:
    def __init__(self, board):
        self.board = board
        self.size = board.size
        self.colorCount = len(board.distinctColors)
        self.result = [None for _ in range(self.colorCount)]
        self.color_to_index = {color: idx for idx, color in enumerate(board.distinctColors)}

    def is_safe(self, row, col):
        # Check if any queen is already placed in this position
        if self.board.grid[row][col].isQueenPlaced:
            return False

        # Check row
        for j in range(self.size):
            if self.board.grid[row][j].isQueenPlaced:
                return False

        # Check column
        for i in range(self.size):
            if self.board.grid[i][col].isQueenPlaced:
                return False

        # Check diagonals (only adjacent cells)
        # Check top-left diagonal
        if row-1 >= 0 and col-1 >= 0 and self.board.grid[row-1][col-1].isQueenPlaced:
            return False
            
        # Check bottom-right diagonal
        if row+1 < self.size and col+1 < self.size and self.board.grid[row+1][col+1].isQueenPlaced:
            return False
            
        # Check top-right diagonal
        if row-1 >= 0 and col+1 < self.size and self.board.grid[row-1][col+1].isQueenPlaced:
            return False
            
        # Check bottom-left diagonal
        if row+1 < self.size and col-1 >= 0 and self.board.grid[row+1][col-1].isQueenPlaced:
            return False

        return True

    def solve_util(self, color_index=0):
        if color_index >= self.colorCount:
            return True

        current_color = list(self.board.distinctColors)[color_index]
        
        for row in range(self.size):
            for col in range(self.size):
                if (self.board.grid[row][col].color == current_color and 
                    self.is_safe(row, col)):
                    # Place queen
                    self.board.grid[row][col].isQueenPlaced = True
                    self.result[color_index] = (row, col)

                    if self.solve_util(color_index + 1):
                        return True

                    # Backtrack
                    self.board.grid[row][col].isQueenPlaced = False
                    self.result[color_index] = None

        return False

    def solve(self):
        if self.solve_util():
            return self.result
        return None