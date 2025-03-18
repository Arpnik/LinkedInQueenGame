import sys
from com.linkedIn.solver.InputProcessor import InputProcessor
from com.linkedIn.solver.OutputProcessor import OutputProcessor
from com.linkedIn.solver.Solver import Solver

def main():
    arguments = len(sys.argv)
    if arguments < 2:
        raise Exception("Please enter the grid image as a command line argument")

    image_path = sys.argv[1]
    processor = InputProcessor(image_path)
    grid, current_grid = processor.extract_grid_colors()
    solver = Solver(current_grid)
    solver.solve()
    out = OutputProcessor(current_grid)
    out.draw_grid()

if __name__ == "__main__":
    main()
