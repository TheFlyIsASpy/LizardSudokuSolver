import math

def CreateSudokuGrid(box_size):
    try:
        box_size = int(box_size)
    except:
        return

    grid = {"notes" : [], "solution" : [], "box_size" : box_size, "solution_log": [], "row_sets" : set(), "column_sets" : set(), "box_sets" : set(), "x_wings" : set(), "pointed_sets": set(), "box_restrictions" : set(), "y_wings": set()}

    size = box_size ** 2

    for _ in range(size):
        note_row = []
        solution_row = []
        for _ in range(size):
            col = []
            for _ in range(size):
                col.append(True)
            note_row.append(col)
            solution_row.append(0)
        grid["notes"].append(note_row)
        grid["solution"].append(solution_row)
    
    return grid

def PlaceNumber(grid, number, x, y):
    
    try:
        number = int(number)
        x = int(x)
        y = int(y)
    except:
        return -1
    
    if number == 0:
        return grid
    
    grid_length = len(grid["solution"])
    
    if grid_length == 0:
        error = "Grid Length Is Zero, make a grid first"
        raise Exception(error)
    
    if grid_length < x:
        error = "trying to place number past maximum row. row: " + str(x) + " x: " + str(x)
        raise Exception(error)
    
    if grid_length < y:
        error = "trying to place number past maximum column col: " + str(y) + " y: " + str(y)
        raise Exception(error)
    
    if number > grid_length:
        error = "trying to place a number larger than the grid size number: " + str(number) + " grid_length: " + str(grid_length)
        raise Exception(error)
    
    if grid["solution"][x][y] != 0:
        if grid["solution"][x][y] != number:
            error = "Two different solutions for the same square solution 1: " + str(grid["solution"][x][y]) + " solution 2: " + str(number) + " x: " + str(x) + " y: " + str(y)
            raise Exception(error)
        else:
            return grid
    
    grid["solution"][x][y] = number
    grid["solution_log"].append("Placing number: " + str(number) + " at row: " + str(x) + " col: " + str(y))

    for i in range(grid_length):
        grid["notes"][x][y][i] = False
    
    grid = RemovePossibleFromRow(grid, number, x)
    grid = RemovePossibleFromColumn(grid, number, y)
    grid = RemovePossibleFromBox(grid, number, x, y)
    
    for i in range(grid_length):
        grid = PerformPointChecks(grid, x, i)
        grid = PerformPointChecks(grid, i, y)

    return grid

def RemovePossibleFromRow(grid, number, x):
    grid_length = grid["box_size"] ** 2
    for i in range(grid_length):
        if grid["notes"][x][i][number - 1]:
            grid["solution_log"].append("Removing possible " + str(number) + " from row: " + str(x) + " column: " + str(i))
            grid["notes"][x][i][number - 1] = False
    return grid

def RemovePossibleFromColumn(grid, number, y):
    grid_length = grid["box_size"] ** 2
    for i in range(grid_length):
        if grid["notes"][i][y][number - 1]:
            grid["solution_log"].append("Removing possible " + str(number) + " from row: " + str(i) + " column: " + str(y))
            grid["notes"][i][y][number - 1] = False
    return grid

def RemovePossibleFromBox(grid, number, x, y):
    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    num_removed = 0
    for i in range(x_min, x_min + grid["box_size"]):
        for j in range(y_min, y_min + grid["box_size"]):
            if grid["notes"][i][j][number - 1]:
                num_removed += 1
                grid["solution_log"].append("Removing possible " + str(number) + " from row: " + str(i) + " col: " + str(j))
                grid["notes"][i][j][number - 1] = False
    
    if num_removed > 0:
        for i in range(x_min, x_min + grid["box_size"]):
            for j in range(y_min, y_min + grid["box_size"]):
                grid = PerformPointChecks(grid, i, j)
    
    return grid

def PerformBasicRowChecks(grid, x):
    grid = CheckRowForOnlyOptions(grid, x)
    grid = CheckRowForOnlyPositions(grid, x)
    grid = CheckRowForSets(grid, x)
    for i in range(grid["box_size"]):
        y = i * grid["box_size"]
        grid = CheckBoxForPointedSets(grid, x, y)
        grid = CheckBoxForRowOrColumnRestrictedSets(grid, x, y)
    return grid

def PerformBasicColumnChecks(grid, y):
    grid = CheckColumnForOnlyOptions(grid, y)
    grid = CheckColumnForOnlyPositions(grid, y)
    grid = CheckColumnForSets(grid, y)
    for i in range(grid["box_size"]):
        x = i * grid["box_size"]
        grid = CheckBoxForPointedSets(grid, x, y)
        grid = CheckBoxForRowOrColumnRestrictedSets(grid, x, y)
    return grid

def PerformBasicBoxChecks(grid, x, y):
    grid = CheckBoxForOnlyOptions(grid, x, y)
    grid = CheckBoxForOnlyPositions(grid, x, y)
    grid = CheckBoxForSets(grid, x, y)
    grid = CheckBoxForPointedSets(grid, x, y)
    grid = CheckBoxForRowOrColumnRestrictedSets(grid, x, y)
    return grid

def PerformBasicPointChecks(grid, x, y):
    grid = PerformBasicRowChecks(grid, x)
    grid = PerformBasicColumnChecks(grid, y)
    grid = PerformBasicBoxChecks(grid, x, y)
    return grid

def PerformAdvancedRowChecks(grid, y):
    for i in range(grid["box_size"] ** 2):
        grid = CheckPointForXWings(grid, i, y)
        grid = CheckPointForYWings(grid, i, y)
    return grid

def PerformAdvancedColumnChecks(grid, x):
    for i in range(grid["box_size"] ** 2):
        grid = CheckPointForXWings(grid, x, i)
        grid = CheckPointForYWings(grid, x, i)
    return grid

def PerformAdvancedPointChecks(grid, x, y):
    grid = PerformAdvancedRowChecks(grid, x)
    grid = PerformAdvancedColumnChecks(grid, y)
    return grid

def PerformPointChecks(grid, x, y):
    grid = PerformBasicPointChecks(grid, x, y)
    grid = PerformAdvancedPointChecks(grid, x, y)
    return grid

def CheckRowForOnlyOptions(grid, x):
        
    grid_length = len(grid["solution"])

    for i in range(grid_length):
        if grid["solution"][x][i] != 0:
            continue
        num_true = 0
        true_number = 0
        for j in range(grid_length):
            if grid["notes"][x][i][j]:
                num_true += 1
                true_number = j + 1
        
        if num_true == 1:
            grid["solution_log"].append("Only row option left number: " + str(true_number) + " at row: " + str(x) + " col: " + str(i))
            grid = PlaceNumber(grid, true_number, x, i)
    
    return grid

def CheckColumnForOnlyOptions(grid, y):
    grid_length = len(grid["solution"])

    for i in range(grid_length):
        if grid["solution"][i][y] != 0:
            continue
        num_true = 0
        true_number = 0
        for j in range(grid_length):
            if grid["notes"][i][y][j]:
                num_true += 1
                true_number = j + 1
        
        if num_true == 1:
            grid["solution_log"].append("Only column option left number: " + str(true_number) + " at row: " + str(i) + " col: " + str(y))
            grid = PlaceNumber(grid, true_number, i, y)
    
    return grid

def CheckBoxForOnlyOptions(grid, x, y):

    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    grid_length = len(grid["solution"])

    for i in range(x_min, x_min + grid["box_size"]):
        for j in range(y_min, y_min + grid["box_size"]):
            if grid["solution"][i][j] != 0:
                continue
            num_true = 0
            true_number = 0
            for k in range(grid_length):
                if grid["notes"][i][j][k]:
                    num_true += 1
                    true_number = k + 1
            
            if num_true == 1:
                grid["solution_log"].append("Only box option left number: " + str(true_number) + " at row: " + str(i) + " col: " + str(j))
                grid = PlaceNumber(grid, true_number, i, j)
    return grid

def CheckRowForOnlyPositions(grid, x):
    grid_length = len(grid["solution"])
    numbers = []
    for i in range(grid_length):
        numbers.append(-1)

    for i in range(grid_length):
        for j in range(grid_length):
            if grid["notes"][x][i][j]:
                if numbers[j] > -1:
                    numbers[j] = -2
                else:
                    if numbers[j] > -2:
                        numbers[j] = i
            

    for i in range(len(numbers)):
        if numbers[i] >= 0:
            grid["solution_log"].append("Only row position left number: " + str(i+1) + " at row: " + str(x) + " col: " + str(numbers[i]))
            grid = PlaceNumber(grid, i+1, x, numbers[i])
    
    return grid

def CheckColumnForOnlyPositions(grid, y):
    grid_length = len(grid["solution"])
    numbers = []
    for i in range(grid_length):
        numbers.append(-1)

    for i in range(grid_length):
        for j in range(grid_length):
            if grid["notes"][i][y][j]:
                if numbers[j] > -1:
                    numbers[j] = -2
                else:
                    if numbers[j] > -2:
                        numbers[j] = i

    for i in range(len(numbers)):
        if numbers[i] >= 0:
            grid["solution_log"].append("Only row position left number: " + str(i+1) + " at row: " + str(numbers[i]) + " col: " + str(y))
            grid = PlaceNumber(grid, i+1, numbers[i], y)
    
    return grid

def CheckBoxForOnlyPositions(grid, x, y):
    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    grid_length = len(grid["solution"])

    numbers = []
    for i in range(grid_length):
        numbers.append(None)

    for i in range(x_min, x_min + grid["box_size"]):
        for j in range(y_min, y_min + grid["box_size"]):
            for k in range(grid_length):
                if grid["notes"][i][j][k]:
                    if numbers[k] != None:
                        numbers[k] = -1
                    else:
                        if numbers[k] != -1:
                            numbers[k] = (i,j)

    for i in range(len(numbers)):
        if numbers[i] != None and numbers[i] != -1:
            grid["solution_log"].append("Only box position left number: " + str(i+1) + " at row: " + str(numbers[i][0]) + " col: " + str(numbers[i][1]))
            grid = PlaceNumber(grid, i+1, numbers[i][0], numbers[i][1])
    
    return grid

def CheckRowForSets(grid, x):
    sets = {}

    grid_length = len(grid["solution"])

    useful_set_length = grid_length - 1

    for i in range(grid_length):
        if grid["solution"][x][i] > 0:
            useful_set_length -= 1
            continue

        num_set = set()

        for n in range(grid_length):
            if grid["notes"][x][i][n]:
                num_set.add(n)

        num_set = frozenset(num_set)

        if (x, num_set) in grid["row_sets"]:
            continue
            
        if len(num_set) > useful_set_length:
            continue
        else:
            if num_set in sets:
                sets[num_set].add(i)
            else:
                sets[num_set] = set()

            for key in sets.keys():
                if num_set.issubset(key):
                    sets[key].add(i)
                if key.issubset(num_set):
                    for c in sets[key]:
                        sets[num_set].add(c)
    
    changed = set()

    for num_set in sets.keys():
        if len(sets[num_set]) > useful_set_length:
            continue

        if len(num_set) > len(sets[num_set]):
            continue
        
        grid["row_sets"].add((x, num_set))

        grid["solution_log"].append("found row solution set for row: " + str(x) + " set: " + str({num + 1 for num in num_set}))

        num_changed = 0;
        for c in range(grid_length):
            if c not in sets[num_set]:
                for n in num_set:
                    if grid["notes"][x][c][n]:
                        num_changed += 1
                        changed.add((x,c))
                        grid["solution_log"].append("row solution set removed: " + str(n + 1) + " at row: " + str(x) + " col: " + str(c))
                        grid["notes"][x][c][n] = False
        
        if num_changed == 0:
            grid["solution_log"].pop()

    if len(changed) > 0:
        for p in changed:
            grid = PerformPointChecks(grid, p[0], p[1])

    return grid

def CheckColumnForSets(grid, y):
    sets = {}

    grid_length = len(grid["solution"])

    useful_set_length = grid_length - 1

    for i in range(grid_length):
        if grid["solution"][i][y] > 0:
            useful_set_length -= 1
            continue

        num_set = set()

        for n in range(grid_length):
            if grid["notes"][i][y][n]:
                num_set.add(n)

        num_set = frozenset(num_set)

        if (y, num_set) in grid["column_sets"]:
            continue
            
        if len(num_set) > useful_set_length:
            continue
        else:
            if num_set in sets:
                sets[num_set].add(i)
            else:
                sets[num_set] = set()

            for key in sets.keys():
                if num_set.issubset(key):
                    sets[key].add(i)
                if key.issubset(num_set):
                    for c in sets[key]:
                        sets[num_set].add(c)
    
    changed = set()

    for num_set in sets.keys():
        if len(sets[num_set]) > useful_set_length:
            continue

        if len(num_set) > len(sets[num_set]):
            continue
        
        grid["column_sets"].add((y, num_set))
        grid["solution_log"].append("found column solution set for collumn: " + str(y) + " set: " + str({num + 1 for num in num_set}))
        
        num_changed = 0
        for r in range(grid_length):
            if r not in sets[num_set]:
                for n in num_set:
                    if grid["notes"][r][y][n]:
                        num_changed += 1
                        changed.add((r,y))
                        grid["solution_log"].append("row solution set removed: " + str(n + 1) + " at row: " + str(r) + " col: " + str(y))
                        grid["notes"][r][y][n] = False

        if num_changed == 0:
            grid["solution_log"].pop()
    
    if len(changed) > 0:
        for p in changed:
            grid = PerformPointChecks(grid, p[0], p[1])

    return grid

def CheckBoxForSets(grid, x, y):

    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    sets = {}

    grid_length = len(grid["solution"])

    useful_set_length = grid_length - 1

    for i in range(x_min, x_min + grid["box_size"]):
        for j in range(y_min, y_min + grid["box_size"]):
            if grid["solution"][i][j] > 0:
                useful_set_length -= 1
                continue

            num_set = set()

            for n in range(grid_length):
                if grid["notes"][i][j][n]:
                    num_set.add(n)

            num_set = frozenset(num_set)

            if ((x_box, y_box), num_set) in grid["box_sets"]:
                continue
                
            if len(num_set) > useful_set_length:
                continue
            else:
                if num_set in sets:
                    sets[num_set].add((i,j))
                else:
                    sets[num_set] = set()

                for key in sets.keys():
                    if num_set.issubset(key):
                        sets[key].add((i,j))
                    if key.issubset(num_set):
                        for c in sets[key]:
                            sets[num_set].add(c)
    
    changed = set()

    for num_set in sets.keys():
        if len(sets[num_set]) > useful_set_length:
            continue

        if len(num_set) > len(sets[num_set]):
            continue
        
        grid["box_sets"].add(((x_box, y_box), num_set))
        grid["solution_log"].append("found box solution set for box at x: " + str(x) + " y: " + str(y) + " set: " + str({num + 1 for num in num_set}))

        num_changed = 0
        for i in range(x_min, x_min + grid["box_size"]):
            for j in range(y_min, y_min + grid["box_size"]):
                if (i,j) not in sets[num_set]:
                    for n in num_set:
                        if grid["notes"][i][j][n]:
                            num_changed += 1
                            changed.add((i,j))
                            grid["solution_log"].append("box solution set removed: " + str(n + 1) + " at row: " + str(i) + " col: " + str(j))
                            grid["notes"][i][j][n] = False

        if num_changed == 0:
            grid["solution_log"].pop()
    
    if len(changed) > 0:
        for p in changed:
            grid = PerformPointChecks(grid, p[0], p[1])

    return grid

def CheckBoxForPointedSets(grid, x, y):
    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    number_counts = {}

    grid_length = len(grid["solution"])

    changed = set()

    for i in range(x_min, x_min + grid["box_size"]):
        for j in range(y_min, y_min + grid["box_size"]):
            if grid["solution"][i][j] > 0:
                continue
            for k in range(grid_length):
                if grid["notes"][i][j][k] and ((x_box, y_box), k) not in grid["pointed_sets"]:
                    if k in number_counts.keys():
                        number_counts[k].add((i,j))
                    else:
                        number_counts[k] = set()
                        number_counts[k].add((i,j))


    for key in number_counts.keys():
        if len(number_counts[key]) <= 3:
            points = number_counts[key]
            firstRow = next(iter(points))[0]
            firstColumn = next(iter(points))[1]
            isPointedRow = True
            isPointedColumn = True
            for p in points:
                if p[0] != firstRow:
                    isPointedRow = False
                if p[1] != firstColumn:
                    isPointedColumn = False

            if isPointedRow:
                grid["solution_log"].append("found pointed row set for box at x: " + str(x) + " y: " + str(y) + " for number: " + str(key + 1))
                grid["pointed_sets"].add(((x_box, y_box), key))
                num_changed = 0
                for i in range(grid_length):
                    if i < y_min or i >= y_min + grid["box_size"]:
                        if grid["notes"][firstRow][i][key]:
                            num_changed += 1
                            grid["solution_log"].append("pointed row set removed: " + str(key + 1) + " at row: " + str(firstRow) + " col: " + str(i))
                            grid["notes"][firstRow][i][key] = False
                            changed.add((firstRow, i))
                
                if num_changed == 0:
                    grid["solution_log"].pop()
            
            if isPointedColumn:
                grid["solution_log"].append("found pointed column set for box at x: " + str(x) + " y: " + str(y) + " for number: " + str(key + 1))
                grid["pointed_sets"].add(((x_box, y_box), key))
                num_changed = 0
                for i in range(grid_length):
                    if i < x_min or i >= x_min + grid["box_size"]:
                        if grid["notes"][i][firstColumn][key]:
                            num_changed += 1
                            grid["solution_log"].append("pointed column set removed: " + str(key + 1) + " at row: " + str(i) + " col: " + str(firstColumn))
                            grid["notes"][i][firstColumn][key] = False
                            changed.add((i, firstColumn))
                if num_changed == 0:
                    grid["solution_log"].pop()
    
    if len(changed) > 0:
        for p in changed:
            grid = PerformPointChecks(grid, p[0], p[1])

    return grid

def CheckBoxForRowOrColumnRestrictedSets(grid, x, y):
    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    grid_length = len(grid["solution"])

    changes = set()

    for i in range(x_min, x_min + grid["box_size"]):
        numbers_in_row = set()
        for j in range(y_min, y_min + grid["box_size"]):
            for k in range(grid_length):
                if grid["notes"][i][j][k]:
                    numbers_in_row.add(k)

        for j in range(grid_length):
            if j < y_min or j >= y_min + grid["box_size"]:
                toRemove = set()
                for n in numbers_in_row:
                    if grid["notes"][i][j][n]:
                        toRemove.add(n)
                
                for n in toRemove:
                    numbers_in_row.remove(n)
        
        if ((x_box, y_box), frozenset(numbers_in_row)) in grid["box_restrictions"]:
            continue;
        
        if len(numbers_in_row) > 0:
            grid["solution_log"].append("found values restricted to row in box row: " + str(i) + " box_x: " + str(x_box) + " box_y: " + str(y_box) + " numbers: " + str({num + 1 for num in numbers_in_row}))
            grid["box_restrictions"].add(((x_box, y_box), frozenset(numbers_in_row)))
            num_changed = 0
            for n in numbers_in_row:
                for j in range(x_min, x_min + grid["box_size"]):
                    for k in range(y_min, y_min + grid["box_size"]):
                        if j != i and grid["notes"][j][k][n]:
                            num_changed += 1
                            grid["solution_log"].append("restricted box row removed: " + str(n + 1) + " at row: " + str(j) + " col: " + str(k))
                            grid["notes"][j][k][n] = False
                            changes.add((j,k))
            if num_changed == 0:
                    grid["solution_log"].pop()
    
    for i in range(y_min, y_min + grid["box_size"]):
        numbers_in_col = set()
        for j in range(x_min, x_min + grid["box_size"]):
            for k in range(grid_length):
                if grid["notes"][j][i][k]:
                    numbers_in_col.add(k)

        for j in range(grid_length):
            if j < x_min or j >= x_min + grid["box_size"]:
                toRemove = set()
                for n in numbers_in_col:
                    if grid["notes"][j][i][n]:
                        toRemove.add(n)
                
                for n in toRemove:
                    numbers_in_col.remove(n)

        if ((x_box, y_box), frozenset(numbers_in_col)) in grid["box_restrictions"]:
            continue;
        
        if len(numbers_in_col) > 0:
            grid["solution_log"].append("found values restricted to column in box column: " + str(i) + " box_x: " + str(x_box) + " box_y: " + str(y_box) + " numbers: " + str({num + 1 for num in numbers_in_col}))
            grid["box_restrictions"].add(((x_box, y_box), frozenset(numbers_in_col)))
            num_changed = 0
            for n in numbers_in_col:
                for j in range(x_min, x_min + grid["box_size"]):
                    for k in range(y_min, y_min + grid["box_size"]):
                        if k != i and grid["notes"][j][k][n]:
                            num_changed += 1
                            grid["solution_log"].append("restricted box column removed: " + str(n + 1) + " at row: " + str(j) + " col: " + str(k))
                            grid["notes"][j][k][n] = False
                            changes.add((j,k))
            if num_changed == 0:
                    grid["solution_log"].pop()
    
    if len(changes) > 0:
        for p in changes:
            grid = PerformPointChecks(grid, p[0], p[1])
    
    return grid

def CheckPointForXWings(grid, x, y):

    grid_length = grid["box_size"] ** 2

    changed = set()

    number_counts = {}

    for i in range(grid_length):
        if grid["notes"][x][y][i]:
            if not (x,y,i) in grid["x_wings"]:
                number_counts[i] = set()

    if len(number_counts.keys()) == 0:
        return grid
    
    for i in range(grid_length):
        for j in range(grid_length):
            if grid["notes"][x][i][j]:
                if j in number_counts:
                    number_counts[j].add(i)

    candidates = []

    for key in number_counts.keys():
        if len(number_counts[key]) == 2:
            candidates.append(key)

    if len(candidates) > 0:
        for i in range(grid_length):
            if i != x:
                candidate_number_counts = {}
                for k in candidates:
                    candidate_number_counts[k] = set()
                for j in range(grid_length):
                    for k in candidates:
                        if grid["notes"][i][j][k]:
                            candidate_number_counts[k].add(j)
                
                for key in candidate_number_counts.keys():
                    if len(candidate_number_counts[key]) == 2:
                        if candidate_number_counts[key] == number_counts[key]:
                            grid["solution_log"].append("found an xwing for " + str(key + 1) + " on rows: " + str({i, x}) + " and columns: " + str(number_counts[key]))
                            num_changed = 0
                            for c in number_counts[key]:
                                grid["x_wings"].add((i, c, key))
                                grid["x_wings"].add((x, c, key))

                            for j in range(grid_length):
                                if j != x and j != i:
                                    for c in number_counts[key]:
                                        num_changed += 1
                                        grid["solution_log"].append("xwing removed " + str(key + 1) + " from row: " + str(j) + " and column: " + str(c))
                                        grid["notes"][j][c][key] = False
                                        changed.add((j,c))
                            if num_changed == 0:
                                grid["solution_log"].pop()
    
    number_counts = {}

    for i in range(grid_length):
        if grid["notes"][x][y][i]:
            number_counts[i] = set()
    
    for i in range(grid_length):
        for j in range(grid_length):
            if grid["notes"][i][y][j]:
                if j in number_counts:
                    number_counts[j].add(i)

    candidates = []

    if len(candidates) > 0:
        for key in number_counts.keys():
            if len(number_counts[key]) == 2:
                candidates.append(key)

        for i in range(grid_length):
            if i != y:
                candidate_number_counts = {}
                for k in candidates:
                    candidate_number_counts[k] = set()
                for j in range(grid_length):
                    for k in candidates:
                        if grid["notes"][j][i][k]:
                            candidate_number_counts[k].add(j)
                
                for key in candidate_number_counts.keys():
                    if len(candidate_number_counts[key]) == 2:
                        if candidate_number_counts[key] == number_counts[key]:
                            grid["solution_log"].append("found an xwing for " + str(key + 1) + " on rows: " + str({number_counts[key]}) + " and columns: " + str({i, y}))
                            num_changed = 0
                            for r in number_counts[key]:
                                grid["x_wings"].add((r, i, key))
                                grid["x_wings"].add((r, y, key))

                            for j in range(grid_length):
                                if j != y and j != i:
                                    for r in number_counts[key]:
                                        num_changed += 1
                                        grid["solution_log"].append("xwing removed: " + str(key + 1) + " on rows: " + str({number_counts[key]}) + " and columns: " + str({i, y}))
                                        grid["notes"][r][j][key] = False
                                        changed.add((r,j))
                            if num_changed == 0:
                                grid["solution_log"].pop()

    if len(changed) > 0:
        for p in changed:
            grid = PerformPointChecks(grid, p[0], p[1])
    
    return grid;

def CheckPointForYWings(grid, x, y):
    x_box = math.ceil((x+1)/grid["box_size"])
    y_box = math.ceil((y+1)/grid["box_size"])

    x_min = grid["box_size"] * (x_box - 1)
    y_min = grid["box_size"] * (y_box - 1)

    grid_length = grid["box_size"] ** 2

    changed = set()

    current_notes = []

    for i in range(grid_length):
        if grid["notes"][x][y][i]:
            current_notes.append(i)

    if len(current_notes) != 2:
        return grid
    
    current_point = (x,y)
    
    potential_ywings = {}

    potential_ywings[current_point] = []

    cached_notes = {}

    for i in range(grid_length):
        if i != x:
            target_notes = set()
            for j in range(grid_length):
                if grid["notes"][i][y][j]:
                    target_notes.add(j)
            
            if len(target_notes) != 2:
                continue

            if (current_notes[0] in target_notes and current_notes[1] not in target_notes) or (current_notes[1] in target_notes and current_notes[0] not in target_notes):
                point = (i,y)
                cached_notes[point] = list(target_notes)
                
                if point in potential_ywings.keys():
                    potential_ywings[point].append(current_point)
                else:
                    potential_ywings[point] = [current_point]
                potential_ywings[current_point].append(point)
    
    for i in range(grid_length):
        if i != y:
            target_notes = set()
            for j in range(grid_length):
                if grid["notes"][x][i][j]:
                    target_notes.add(j)
            
            if len(target_notes) != 2:
                continue

            if (current_notes[0] in target_notes and current_notes[1] not in target_notes) or (current_notes[1] in target_notes and current_notes[0] not in target_notes):
                point = (x,i)
                cached_notes[point] = list(target_notes)
                if point in potential_ywings.keys():
                    potential_ywings[point].append(current_point)
                else:
                    potential_ywings[point] = [current_point]
                potential_ywings[current_point].append(point)

    for i in range(x_min, x_min + grid["box_size"]):
        for j in range(y_min, y_min + grid["box_size"]):
            if i != x and j != y:
                target_notes = set()
                for k in range(grid_length):
                    if grid["notes"][i][j][k]:
                        target_notes.add(k)
                
                if len(target_notes) != 2:
                    continue

                if (current_notes[0] in target_notes and current_notes[1] not in target_notes) or (current_notes[1] in target_notes and current_notes[0] not in target_notes):
                    point = (i,j)
                    cached_notes[point] = list(target_notes)
                    if point in potential_ywings.keys():
                        potential_ywings[point].append(current_point)
                    else:
                        potential_ywings[point] = [current_point]
                    potential_ywings[current_point].append(point)


    for p in potential_ywings.keys():
        if p == (x,y):
            continue

        p_x_box = math.ceil((p[0]+1)/grid["box_size"])
        p_y_box = math.ceil((p[1]+1)/grid["box_size"])

        p_x_min = grid["box_size"] * (p_x_box - 1)
        p_y_min = grid["box_size"] * (p_y_box - 1)

        if current_notes[0] == cached_notes[p][0] or current_notes[0] == cached_notes[p][1]:
            matching_num = current_notes[0]
            mismatching_num = current_notes[1]
        else:
            matching_num = current_notes[1]
            mismatching_num = current_notes[0]

        for i in range(grid_length):
            if i != p[0]:
                target_point = (i, p[1])
                if target_point in cached_notes.keys():
                    target_notes = set(cached_notes[target_point])
                else:
                    target_notes = set()
                    for j in range(grid_length):
                        if grid["notes"][i][p[1]][j]:
                            target_notes.add(j)
                
                if len(target_notes) != 2:
                    continue

                if mismatching_num in target_notes and matching_num not in target_notes and ((cached_notes[p][0] in target_notes) ^ (cached_notes[p][1] in target_notes)):
                    cached_notes[target_point] = list(target_notes)
                    potential_ywings[p].append(target_point)
        
        for i in range(grid_length):
            if i != p[1]:
                target_point = (p[0], i)
                if target_point in cached_notes.keys():
                    target_notes = set(cached_notes[target_point])
                else:
                    target_notes = set()
                    for j in range(grid_length):
                        if grid["notes"][p[0]][i][j]:
                            target_notes.add(j)
                
                if len(target_notes) != 2:
                    continue

                if mismatching_num in target_notes and matching_num not in target_notes and ((cached_notes[p][0] in target_notes) ^ (cached_notes[p][1] in target_notes)):
                    cached_notes[target_point] = list(target_notes)
                    potential_ywings[p].append(target_point)

        for i in range(p_x_min, p_x_min + grid["box_size"]):
            for j in range(p_y_min, p_y_min + grid["box_size"]):
                if i != p[0] and j != p[1]:
                    target_point = (i,j)
                    if target_point in cached_notes.keys():
                        target_notes = set(cached_notes[target_point])
                    else:
                        target_notes = set()
                        for k in range(grid_length):
                            if grid["notes"][i][j][k]:
                                target_notes.add(k)
                    
                    if len(target_notes) != 2:
                        continue

                    if mismatching_num in target_notes and matching_num not in target_notes and ((cached_notes[p][0] in target_notes) ^ (cached_notes[p][1] in target_notes)):
                        cached_notes[target_point] = list(target_notes)
                        potential_ywings[p].append(target_point)

    y_wings = []

    for i in range(len(potential_ywings[current_point])):
        target_wing = potential_ywings[current_point][i]
        if cached_notes[target_wing][0] == current_notes[0] or cached_notes[target_wing][0] == current_notes[1]:
            matching_num = cached_notes[target_wing][0]
            mismatching_num = cached_notes[target_wing][1]
        else:
            matching_num = cached_notes[target_wing][1]
            mismatching_num = cached_notes[target_wing][0]

        for j in range(i+1, len(potential_ywings[current_point])):
            second_wing = potential_ywings[current_point][j]
            if (current_point, target_wing, second_wing) in grid["y_wings"] or (current_point, second_wing, target_wing) in grid["y_wings"]:
                continue
            if (cached_notes[second_wing][0] == mismatching_num and cached_notes[second_wing][1] != matching_num) or (cached_notes[second_wing][1] == mismatching_num and cached_notes[second_wing][0] != matching_num):
                grid["y_wings"].add((current_point, target_wing, second_wing))
                grid["y_wings"].add((current_point, second_wing, target_wing))
                y_wings.append((current_point, target_wing, second_wing, mismatching_num))

    for p in potential_ywings.keys():
        if p != current_point:
            for i in range(1, len(potential_ywings[p])):
                if (p, current_point, potential_ywings[p][i]) in grid["y_wings"] or (p, potential_ywings[p][i], current_point) in grid["y_wings"]:
                    continue
                if current_notes[0] == cached_notes[p][0] or current_notes[0] == cached_notes[p][1]:
                    mismatching_num = current_notes[1]
                else:
                    mismatching_num = current_notes[0]
                grid["y_wings"].add((p, current_point, potential_ywings[p][i]))
                grid["y_wings"].add((p, potential_ywings[p][i], current_point))
                y_wings.append((p, current_point, potential_ywings[p][i], mismatching_num))

    for y_wing in y_wings:

        grid["solution_log"].append("found a ywing for pivot: " + str(y_wing[0]) + " wing1: " + str(y_wing[1]) + " wing2: " + str(y_wing[2]) + " for numbers: " + str(y_wing[3] + 1))
        
        num_changed = 0

        w1 = y_wing[1]
        w2 = y_wing[2]
        to_eliminate = y_wing[3]

        w1_x_box = math.ceil((w1[0]+1)/grid["box_size"])
        w1_y_box = math.ceil((w1[1]+1)/grid["box_size"])

        w1_x_min = grid["box_size"] * (w1_x_box - 1)
        w1_y_min = grid["box_size"] * (w1_y_box - 1)

        w2_x_box = math.ceil((w2[0]+1)/grid["box_size"])
        w2_y_box = math.ceil((w2[1]+1)/grid["box_size"])

        w2_x_min = grid["box_size"] * (w2_x_box - 1)
        w2_y_min = grid["box_size"] * (w2_y_box - 1)

        crossover_points = set()

        crossover_points.add((w1[0], w2[1]))
        crossover_points.add((w2[0], w1[1]))

        if w1[0] >= w2_x_min and w1[0] < w2_x_min + grid["box_size"]:
            for i in range(w2_y_min, w2_y_min + grid["box_size"]):
                crossover_points.add((w1[0], i))
        
        if w1[1] >= w2_y_min and w1[1] < w2_y_min + grid["box_size"]:
            for i in range(w2_x_min, w2_x_min + grid["box_size"]):
                crossover_points.add((i, w1[1]))

        if w2[0] >= w1_x_min and w2[0] < w1_x_min + grid["box_size"]:
            for i in range(w1_y_min, w1_y_min + grid["box_size"]):
                crossover_points.add((w2[0], i))
        
        if w2[1] >= w1_y_min and w2[1] < w1_y_min + grid["box_size"]:
            for i in range(w1_x_min, w1_x_min + grid["box_size"]):
                crossover_points.add((i, w2[1]))

        if y_wing[0] in crossover_points:
            crossover_points.remove(y_wing[0])

        if y_wing[1] in crossover_points:
            crossover_points.remove(y_wing[1])

        if y_wing[2] in crossover_points:
            crossover_points.remove(y_wing[2])

        for p in crossover_points:
            if grid["notes"][p[0]][p[1]][to_eliminate]:
                num_changed += 1
                grid["solution_log"].append("ywing elmiminated: " + str(to_eliminate + 1) + " from row: " + str(p[0]) + " column: " + str(p[1]))
                grid["notes"][p[0]][p[1]][to_eliminate] = False
                changed.add(p)

        if num_changed == 0:
            grid["solution_log"].pop()

    if len(changed) > 0:
        for p in changed:
            grid = PerformPointChecks(grid, p[0], p[1])
    
    return grid

def PrintSolution(grid):
    for r in grid["solution"]:
        print(r)
    print()

def PrintNotes(grid):
    for r in grid["notes"]:
        for c in r:
            numbers = []
            for i in range(len(c)):
                if c[i]:
                    numbers.append(i+1)
            print(numbers)
        print()
        print()

def PrintSolutionLog(grid):
    for s in grid["solution_log"]:
        print(s)
