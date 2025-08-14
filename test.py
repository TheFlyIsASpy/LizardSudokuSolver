import LizardSudokuSolver as s

debug_solution = [
    [3,6,2,8,5,4,7,9,1],
    [5,9,4,7,6,1,2,3,8],
    [8,7,1,3,2,9,4,6,5],
    [9,2,3,6,1,8,5,7,4],
    [4,1,5,9,7,2,6,8,3],
    [7,8,6,5,4,3,1,2,9],
    [2,5,8,1,3,7,9,4,6],
    [6,4,9,2,8,5,3,1,7],
    [1,3,7,4,9,6,8,5,2],
]

debug_solution_points = set()

for i in range(len(debug_solution)):
    for j in range(len(debug_solution)):
        debug_solution_points.add((i,j,debug_solution[i][j]))

grid = s.CreateSudokuGrid(3)

puzzle = [
    [0,0,0,0,0,0,0,0,1],
    [0,0,4,0,6,0,2,0,8],
    [0,7,0,3,2,0,4,0,0],
    [9,0,0,0,1,8,0,0,0],
    [0,0,5,0,0,0,6,0,0],
    [0,0,0,5,4,0,0,0,9],
    [0,0,8,0,3,7,0,4,0],
    [6,0,9,0,8,0,3,0,0],
    [1,0,0,0,0,0,0,0,0],
]


for i in range(len(puzzle)):
    for j in range(len(puzzle[i])):
        
        if puzzle[i][j] > 0:
            grid = s.PlaceNumber(grid, puzzle[i][j], i, j)


s.PrintSolutionLog(grid)
s.PrintSolution(grid)
