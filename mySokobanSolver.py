
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(10414291, 'Byron', 'Chiu'), (11079550, 'Declan', 'Bengtson')]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#Cell definitions
cells = {"empty": " ",
         "box": "$",
         "wall": "#",
         "taboo": "X",
         "target": ".",
         "worker": "@",
         "box_target": "*",
         "worker_target": "!",
         "removed": ['$', '@'], 
         "three_targets": ['.', '*', '!']
         }

#Definitions of directions
direction = {"Up": (0,-1), "Down": (0,1), "Left": (-1,0), "Right": (1,0)}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Utility functions
def coordinate_movement_2d(loc, delta):
    """
    @param loc: location of coordinate
    @param delta: The moving transformation
    
    @return
         The final location after a moving transformation
         in the 2D coordinate space.
    """
    return (loc[0] + delta[0], loc[1] + delta[1])

def manhattan_distance(location1, location2):
    '''
    @param location1: First location
    @param location2: Second location
    
    @return
        Return xy distance between two points 
    '''
    return abs((location1[0] - location2[0])) + abs((location1[1] - location2[1]))
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    
    def checkforcorner(idx, walls):
        """
        Examines if the Up, Down, Left and Right sides cell is a wall mark
        in order to determine wether its a corner.
        @param idx: index of the current cell
        @param walls: a list of walls
        
        @return
            True if it is a corner
            False if it is not a corner
        
        """
        if coordinate_movement_2d(idx, direction["Left"]) in walls \
            and coordinate_movement_2d(idx, direction["Down"]) in walls:
            return True
        if coordinate_movement_2d(idx, direction["Right"]) in walls \
            and coordinate_movement_2d(idx, direction["Down"]) in walls:
            return True
        if coordinate_movement_2d(idx, direction["Left"]) in walls \
            and coordinate_movement_2d(idx, direction["Up"]) in walls:
            return True
        if coordinate_movement_2d(idx, direction["Right"]) in walls \
            and coordinate_movement_2d(idx, direction["Up"]) in walls:
            return True
        
        return False #If not a corner returns false

    def checkforwall(idx, walls):
        """
        Check if a cell has a wall in the up, down, left, right direction.
        @param idx: index of the current cell
        @param walls: a list of walls
        
        @return
            True if in any direction of the cell there is a wall
        """
        return coordinate_movement_2d(idx, direction["Down"]) in walls \
            or coordinate_movement_2d(idx, direction["Up"]) in walls \
            or coordinate_movement_2d(idx, direction["Right"]) in walls \
            or coordinate_movement_2d(idx, direction["Left"]) in walls 
            
    walls = warehouse.walls #initialise a variable for the warehouse walls
    str_warehouse = str(warehouse) # convert the warehouse to a string

    #Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
    for cell in cells["removed"]:
        str_warehouse = str_warehouse.replace(cell, " ")
    warehousematrix = [list(line) for line in str_warehouse.splitlines()]#converts to 2d matrix
        
    for X in range(warehouse.nrows):# loop through all the rows in a 2d matrix
            side_wall = True
            for Y in range(warehouse.ncols):# loop through all the columns in a 2d matrix
                matrix_index = (Y,X)
                square = warehousematrix[X][Y]
                if side_wall and square == cells["wall"]:
                    side_wall = False
                elif not side_wall:
                    if all([cell == cells["empty"] for cell in warehousematrix[X][Y:]]):
                        break
                    if square == cells["empty"] and checkforcorner(matrix_index, walls):
                            warehousematrix[X][Y] = cells["taboo"]
                            
    #Rule 2: all the cells between two corners along a wall are taboo if none of these cells is a target.
    for X in range(warehouse.nrows):#loop all the rows in a 2d matrix
            for Y in range(warehouse.ncols):# loop all the columns in a 2d matrix
                matrix_index = (Y, X)
                square = warehousematrix[X][Y]
                if square == cells["taboo"] and checkforcorner(matrix_index, walls):
                    row_cont = warehousematrix[X][Y+1:]
                    col_cont = [row[Y] for row in warehousematrix[X+1:]]
                    row_list = enumerate(row_cont)
                    col_list = enumerate(col_cont)
                    for index, value in row_list:
                        if value == cells["wall"] or value in cells["three_targets"]:
                            break
                        if value == cells["taboo"] and checkforcorner((Y+index+1, X), walls):
                            if all([checkforwall((location, X), walls) for location in range(Y+1, Y+index+1)]):
                                for location in range(Y+1, Y+index+1):
                                    warehousematrix[X][location] = cells["taboo"]
                    for index, value in col_list:
                        if value == cells["wall"] or value in cells["three_targets"]:
                            break
                        if value == cells["taboo"] and checkforcorner((Y, X+index+1), walls):
                            if all([checkforwall((Y, location), walls) for location in range(X+1, X+index+1)]):
                                for location in range(X+1, X+index+1):
                                    warehousematrix[location][Y] = cells["taboo"]

    #convert to a full string representation
    str_warehouse = '\n'.join(["".join(row) for row in warehousematrix])

    # Swap the three targets with white space
    for cell in cells["three_targets"]:
        str_warehouse = str_warehouse.replace(cell, " ")

    return str_warehouse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.walls = warehouse.walls
        self.boxes = warehouse.boxes
        self.initial = warehouse.worker, tuple(warehouse.boxes)
        self.taboo = [sokoban.find_2D_iterator(taboo_cells(self.warehouse).splitlines(), cells["taboo"])]
        self.weights = warehouse.weights
        self.goal = warehouse.targets

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        action_seq = [] # initialise a list of actions to be returned
        
        #Copy the state of the initial worker and boxes
        worker_state = state[0]
        boxes_state = list(state[1])
        
        # Loop through each possible direction
        for way in direction.keys():
            worker_state2 = coordinate_movement_2d(worker_state, direction.get(way))
            if worker_state2 in self.walls:
                continue
            if worker_state2 in boxes_state:
                box_state2 = coordinate_movement_2d(worker_state2, direction.get(way))
                if box_state2 not in boxes_state and box_state2 not in self.taboo and box_state2 not in self.walls:
                        action_seq.append(way)
            else: 
                action_seq.append(way)
        return action_seq
    

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        
        #Copy the state of the initial worker and boxes
        worker_state = state[0]
        boxes_state = list(state[1])
        
        worker_state2 =  coordinate_movement_2d(worker_state, direction.get(action))

        if worker_state2 in boxes_state:
            box_state2 =  coordinate_movement_2d(worker_state2, direction.get(action))
            box_index = boxes_state.index(worker_state2)
            boxes_state[box_index] = box_state2
        return worker_state2, tuple(boxes_state)

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return set(state[1]) == set(self.goal) 

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        if state1[1] == state2[1]: #box is not pushed
            return c + 1
        else: # box is pushed
            box_number = state1[1].index(state2[0])
            box_weight = self.weights[box_number]
            return c + box_weight + 1

    def h(self, n):
        '''
        The value of the heurtistic utilising Manhattan Distance and the box weights.
        '''
        heur = 0
        worker = n.state[0]
        boxes = list(n.state[1])
        targets = self.goal
        weights = self.weights
        box_list = enumerate(boxes);
        
        for i, box in box_list:
            worker_dist = manhattan_distance(box,worker)
            for target in targets:
                distance = manhattan_distance(box,target) * (1+weights[i])
            heur += distance
            heur += worker_dist
        return heur


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    X, Y = warehouse.worker
    boxes = warehouse.boxes
    walls = warehouse.walls

    for action in action_seq:
        #Action = Left         
        if action == 'Left':
            X2 = X - 1
            Y2 = Y
            if (X2, Y2) in boxes and (X2 - 1, Y2) not in walls:
                    boxes.remove((X2, Y2)) and boxes.append((X2 - 1, Y2))
                    X = X2
            elif (X2, Y2) in walls:
                return 'Impossible'
            else:
                X = X2
        #Action = Right               
        elif action == 'Right':
            X2 = X + 1
            Y2 = Y
            if (X2, Y2) in boxes and (X2 + 1, Y2) not in walls:
                    boxes.remove((X2, Y2)) and boxes.append((X2 + 1, Y2))
                    X = X2
            elif (X2, Y2) in walls:
                return 'Impossible'
            else:
                X = X2
        #Action = Up       
        elif action == 'Up':
            Y2 = Y - 1
            X2 = X
            if (X2, Y2) in boxes and (X2, Y2 - 1) not in walls:
                    boxes.remove((X2, Y2)) and boxes.append((X2, Y2 - 1))
                    Y = Y2  
            elif (X2, Y2) in walls:
                return 'Impossible' 
            else:
                Y = Y2
        #Action = Down       
        elif action == 'Down':
            Y2 = Y + 1
            X2 = X
            if (X2, Y2) in boxes and (X2, Y2 + 1) not in walls:
                    boxes.remove((X2, Y2)) and boxes.append((X2, Y2 + 1))
                    Y = Y2 
            elif (X2, Y2) in walls:
                return 'Impossible'  
            else:
                Y = Y2

    warehouse.worker = X, Y
    return warehouse.__str__()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    #make a copy of the warehouse to be used in the check_elem_action_seq function
    cp_warehouse = warehouse.copy()

    #initialise the warehouse
    temp_sokoban = SokobanPuzzle(warehouse)
    #Solution found using astar_graph_search() 
    Answer = search.astar_graph_search(temp_sokoban)
    move = []

    if Answer is None:
        return 'Impossible', 0 #Returns impossible if no answer is computed
    else:
        #append each action to a list to be used to check the action sequence
        for node in Answer.path():
            move.append(node.action.__str__())
        action_seq = move[1:]
        if check_elem_action_seq(cp_warehouse, action_seq) == 'Impossible':
            return 'Impossible'
        else:
            Solution = Answer.solution() #Gets the action sequence
            Cost = Answer.path_cost  #computes the cost utilising the path_cost function
        return Solution, Cost

