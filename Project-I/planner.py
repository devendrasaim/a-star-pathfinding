import numpy as np
from typing import List, Tuple, Optional
import scipy
import heapq

class Cell:
    def __init__(self):
        # define f, g, and h
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

        self.parent_i = 0
        self.parent_j = 0


def backtrack(cell_info, dest):

    path = []
    r = dest[0]
    c = dest[1]

    while not (cell_info[r][c].parent_i == r and cell_info[r][c].parent_j == c):
        path.append((r,c))
        r = cell_info[r][c].parent_i
        c = cell_info[r][c].parent_j
    
    path.append((r,c))
    path.reverse()
    return path

def a_star_path(grid, start, end):
    
    # define open and closed lists
    row_size = len(grid)
    col_size = len(grid[0])

    visited = [[False for _ in range(col_size)] for _ in range(row_size)]
    cell_info = [[Cell() for _ in range(col_size)] for _ in range(row_size)]

    i = start[0]
    j = start[1]

    # update start cell info
    cell_info[i][j].f = 0
    cell_info[i][j].g = 0
    cell_info[i][j].h = 0
    cell_info[i][j].parent_i = i
    cell_info[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0,i,j))

    found = False

    # lambda functions
    is_valid = lambda r,c, R,C : (r >= 0) and (r < R) and (c >= 0) and (c < C)
    is_unblocked = lambda r,c, G : G[r][c] == 0
    is_visited = lambda r,c, cl : cl[r][c] == True
    is_destination = lambda r,c, des: des[0] == r and des[1] == c

    # euclidean_dist = lambda r,c,des: ((r -des[0])**2 +  (c-des[1])**2) ** 0.5
    euclidean_dist = lambda r,c, des: abs(r-des[0]) + abs(c-des[1])

    while len(open_list) > 0:

        p = heapq.heappop(open_list)
        i = p[1]
        j = p[2]
        visited[i][j] = True

        # check successors in all directions
        surroundings = [[0,1], [0,-1], [-1, 0], [1,0]] # possible choices to take

        for d in surroundings:
            i_prime = d[0] + i
            j_prime = d[1] + j
            
            # if successor is valid, unblocked and not visited
            if is_valid(i_prime, j_prime, row_size, col_size) and is_unblocked(i_prime, j_prime, grid) and not is_visited(i_prime, j_prime, visited):
                if is_destination(i_prime, j_prime, end):
                    # update cell information
                    cell_info[i_prime][j_prime].parent_i = i
                    cell_info[i_prime][j_prime].parent_j = j
                    found = True
                    # print ("Destination path is found")
                    # return path?
                    return backtrack(cell_info, end)
                else:
                    # compute new values
                    g_prime = cell_info[i][j].g + 1.0
                    h_prime = euclidean_dist(i_prime, j_prime,end)
                    f_prime = g_prime + h_prime

                    if cell_info[i_prime][j_prime].f == float('inf') or cell_info[i_prime][j_prime].f > f_prime:
                        # update cell info and push to queue
                        cell_info[i_prime][j_prime].g = g_prime
                        cell_info[i_prime][j_prime].h = h_prime
                        cell_info[i_prime][j_prime].f = f_prime
                        cell_info[i_prime][j_prime].parent_i = i
                        cell_info[i_prime][j_prime].parent_j = j
                        heapq.heappush(open_list, (f_prime, i_prime, j_prime))
    
    if not found:
        print("Failed to find path")

                


def dfs(grid, start, end):
    """A DFS example"""
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    visited = set()
    parent = {start: None}

    # Consider all 8 possible moves (up, down, left, right, and diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Up, Down, Left, Right
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal moves

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            # Reconstruct the path
            path = []
            while (x, y) is not None:
                path.append((x, y))
                if parent[(x, y)] is None:
                    break  # Stop at the start node
                x, y = parent[(x, y)]
            return path[::-1]  # Return reversed path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent[(nx, ny)] = (x, y)

    return None  # Return None if no path is found


# new path using A*.

#def compute_shortest_path()
def plan_path(world: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[np.ndarray]:
    """
    Computes a path from the start position to the end position 
    using a certain planning algorithm (DFS is provided as an example).

    Parameters:
    - world (np.ndarray): A 2D numpy array representing the grid environment.
      - 0 represents a walkable cell.
      - 1 represents an obstacle.
    - start (Tuple[int, int]): The (row, column) coordinates of the starting position.
    - end (Tuple[int, int]): The (row, column) coordinates of the goal position.

    Returns:
    - np.ndarray: A 2D numpy array where each row is a (row, column) coordinate of the path.
      The path starts at 'start' and ends at 'end'. If no path is found, returns None.
    """
    # Ensure start and end positions are tuples of integers
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    # Convert the numpy array to a list of lists for compatibility with the example DFS function
    world_list: List[List[int]] = world.tolist()

    # Perform DFS pathfinding and return the result as a numpy array
    path = a_star_path(world_list, start, end)

    # path2 = dfs(world_list, start, end)
    # path = path2
    # print(len(path) , len(path2))
    return np.array(path) if path else None
