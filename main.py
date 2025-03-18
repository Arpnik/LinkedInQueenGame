import sys
from com.linkedIn.solver.InputProcessor import InputProcessor
from com.linkedIn.solver.OutputProcessor import OutputProcessor
from com.linkedIn.solver.Solver import Solver

def main():
    arguments = len(sys.argv)
    # if arguments < 2:
    #     raise Exception("Please enter the grid image as a command line argument")

    # image_path = sys.argv[1]
    image_path = "/Users/arpniksingh/Desktop/grid-today.png"
    processor = InputProcessor(image_path)
    grid, current_grid = processor.extract_grid_colors()
    solver = Solver(current_grid)
    # print("\n")
    # print(solver.solve())
    out = OutputProcessor(current_grid)
    out.draw_grid()

if __name__ == "__main__":
    main()
