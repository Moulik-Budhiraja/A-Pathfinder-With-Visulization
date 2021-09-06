from TakeInput import take_input
import pygame
import time
import math
import random
pygame.init()


WIDTH, HEIGHT = 600, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)


class GridPos:  # Stores basic data about each square on the grid
    def __repr__(self):
        return f'({self.x}, {self.y})'  # (x, y)

    # Position: (x, y) #  dimensions: (width, height)
    # Requires grid object to find neighbors

    def __init__(self, position: tuple, dimensions: tuple, grid):
        self.x, self.y = position
        self.width, self.height = dimensions

        self.grid = grid

        self.state = "null"  # null, wall, start or end

        # Variables used only during solve
        self.g_cost = None
        self.h_cost = None
        self.f_cost = None
        self.open = "null"  # null, open or closed
        self.solve_path = []
        self.active_neighbors = []

    def clear(self):  # Resets all variables to their original state
        self.g_cost = None
        self.h_cost = None
        self.f_cost = None
        self.open = "null"
        self.solve_path = []
        self.active_neighbors = []

    def get_h_cost(self):  # Gets the direct distance from the current square to the end point
        # Determine where end point is relitive to current square
        end_x, end_y = self.grid.end_point

        difference_x = end_x - self.x
        difference_y = self.y - end_y

        diagonal_dist = min(abs(difference_x), abs(
            difference_y))  # abs -> absolute value
        straight_dist = abs(abs(difference_y) - abs(difference_x))

        self.h_cost = diagonal_dist * 14 + straight_dist * 10

        return self.h_cost

    def get_g_cost(self, target=None):
        if target == None:
            solve_path_positions = [(grid_pos.x, grid_pos.y)
                                    for grid_pos in self.solve_path]

            last_pos = None
            self.g_cost = 0
            for grid_pos in solve_path_positions:
                if last_pos == None:
                    last_pos = grid_pos
                    continue

                last_pos_x, last_pos_y = last_pos
                grid_pos_x, grid_pos_y = grid_pos

                if last_pos_x != grid_pos_x and last_pos_y != grid_pos_y:
                    self.g_cost += 14
                else:
                    self.g_cost += 10

                last_pos = grid_pos

            return self.g_cost

        else:
            solve_path_positions = [(grid_pos.x, grid_pos.y)
                                    for grid_pos in self.solve_path]

            last_pos = None
            g_cost = 0
            for grid_pos in solve_path_positions:
                if last_pos == None:
                    last_pos = grid_pos
                    continue

                last_pos_x, last_pos_y = last_pos
                grid_pos_x, grid_pos_y = grid_pos

                if last_pos_x != grid_pos_x and last_pos_y != grid_pos_y:
                    g_cost += 14
                else:
                    g_cost += 10

                last_pos = grid_pos

            return g_cost

    def get_f_cost(self):
        self.get_h_cost()

        try:
            self.f_cost = self.g_cost + self.h_cost
            return self.f_cost
        except TypeError:
            return None

    def get_active_neighbors(self):
        active_neighbors = []
        rows = self.grid.get_grid()[self.y - 1: self.y + 2]
        neighbors = [row[self.x - 1: self.x + 2] for row in rows]
        neighbors = sum(neighbors, [])  # Combines 3 lists into 1

        neighbors = [
            neighbor for neighbor in neighbors if (neighbor.state == "null" or neighbor.state == "end") and neighbor.open != "closed"]

        for neighbor in neighbors:
            self.set_solve_path(neighbor)
            neighbor.get_g_cost()
            neighbor.get_f_cost()
            neighbor.open = "open"

        self.active_neighbors = neighbors

        return neighbors

    def set_solve_path(self, target):
        if target.solve_path == []:
            target.solve_path = self.solve_path + [target]
        else:
            new_path = self.solve_path + [target]
            if target.g_cost > self.get_g_cost(new_path):
                target.solve_path = new_path


class Grid:
    # dimensions: (width, height) # Requires window object to communicate
    def __init__(self, window, dimensions: tuple):
        self.width, self.height = dimensions
        self.window_width = WIDTH
        self.window_height = HEIGHT

        self.last_changed = (-1, -1)
        self.draw_mode = "add"

        self.window = window

        self.clean_window()
        self.generate_grid()
        self.assign_positions()

    def generate_grid(self):  # Generates a grid with grid_pos objects in each square
        self.grid = []

        for y in range(self.height):
            current_row = []
            for x in range(self.width):
                current_row.append(
                    GridPos((x, y), (self.box_width, self.box_height), self))
            self.grid.append(current_row)

    def clean_window(self):  # Adjusts the window size so there are no black bars
        self.box_width = self.window_width // self.width
        self.box_height = self.window_height // self.height

        new_window_width = self.box_width * self.width
        new_window_height = self.box_height * self.height

        self.window.adjust_window((new_window_width, new_window_height))

    # Creates pygame rectangle objects and assigns them to the correct places on the grid
    def assign_positions(self):
        for row in self.grid:
            for grid_pos in row:
                x_pos = grid_pos.x * grid_pos.width
                y_pos = grid_pos.y * grid_pos.height

                grid_pos.square = pygame.Rect(
                    x_pos, y_pos, grid_pos.width, grid_pos.height)
                grid_pos.square_border = pygame.Rect(
                    x_pos, y_pos, grid_pos.width, grid_pos.height)

    def set_start_point(self, position: tuple):
        self.start_point = position

        for row in self.grid:
            for grid_pos in row:
                if position == (grid_pos.x, grid_pos.y):
                    grid_pos.state = "start"
                    grid_pos.open = "open"
                    grid_pos.solve_path.append(grid_pos)
                    grid_pos.get_g_cost()
                    grid_pos.get_f_cost()

    def set_end_point(self, position: tuple):
        self.end_point = position

        for row in self.grid:
            for grid_pos in row:
                if position == (grid_pos.x, grid_pos.y):
                    grid_pos.state = "end"

    def get_grid(self):
        return self.grid


class Window:
    # Initialize important variables and send self to other objects
    def __init__(self, dimensions: tuple, start_point: tuple, end_point: tuple):
        self.width, self.height = dimensions

        self.WIN = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("A* Pathfinding")

        self.grid = Grid(self, (30, 30))  # ! Change to variables

        self.grid.set_end_point(end_point)
        self.grid.set_start_point(start_point)

    def main(self):  # Where I've chosen to throw everything together

        # Variables to track various states
        self.mouse_down = False
        self.solve = False

        self.run = True
        while self.run:
            self.logic()

            # Reset the board to black at the start of every frame
            self.WIN.fill((0, 0, 0))

            self.draw_core()
            self.draw_visuals()
            pygame.display.update()

    def logic(self):  # Where all of the logical operations take place
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if not self.solve:  # Only allow actions if program is not solving path
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_c:    # Removes all walls from grid
                        for row in self.grid.get_grid():
                            for grid_pos in row:
                                if grid_pos.state == "wall":
                                    grid_pos.state = "null"

                        self.solution = []

                    if event.key == pygame.K_SPACE:
                        self.solve = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True  # Stores left mouse button state

                    for row in self.grid.get_grid():  # Loop through all positions to check which square was clicked
                        for grid_pos in row:
                            # Choose whether to add or subtract squares based on the first square that was clicked
                            if grid_pos.square.collidepoint(event.pos):
                                if grid_pos.state == "null":
                                    self.grid.draw_mode = "add"
                                elif grid_pos.state == "wall":
                                    self.grid.draw_mode = "subtract"
                                break

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False
                    self.grid.last_changed = (None, None)

                if self.mouse_down:  # If mouse is held down start drawing
                    for row in self.grid.get_grid():
                        for grid_pos in row:
                            if grid_pos.square.collidepoint(pygame.mouse.get_pos()):
                                # Only change square state if it wasn't just changed
                                if self.grid.last_changed != (grid_pos.x, grid_pos.y):
                                    self.grid.last_changed = (
                                        grid_pos.x, grid_pos.y)

                                    if self.grid.draw_mode == "add":
                                        if grid_pos.state == "null":
                                            grid_pos.state = "wall"

                                    elif self.grid.draw_mode == "subtract":
                                        if grid_pos.state == "wall":
                                            grid_pos.state = "null"

        if self.solve:
            start_x, start_y = self.grid.start_point
            start_point = self.grid.get_grid()[start_y][start_x]

            open_positions = {start_point}

            while self.solve:

                open_positions_cost = {}

                for position in open_positions:
                    if position.f_cost in open_positions_cost:
                        if position.h_cost < open_positions_cost[position.f_cost].h_cost:
                            open_positions_cost[position.f_cost] = position
                        continue
                    open_positions_cost[position.f_cost] = position

                for row in self.grid.get_grid():
                    for grid_pos in row:
                        if grid_pos.open == "closed":
                            pygame.draw.rect(self.WIN, BLUE, grid_pos.square)
                        elif grid_pos.open == "open":
                            pygame.draw.rect(
                                self.WIN, (128, 0, 128), grid_pos.square)

                pygame.display.update()

                try:
                    best_pos = min(open_positions_cost.keys())
                except ValueError:
                    print("position not solvable")

                    for row in self.grid.get_grid():
                        for grid_pos in row:
                            grid_pos.clear()

                    self.solve = False
                    break

                best_pos = open_positions_cost[best_pos]

                print(best_pos.solve_path, "\n")

                if best_pos.h_cost == 0:
                    self.solve = False
                    self.solution = best_pos.solve_path

                    for row in self.grid.get_grid():
                        for grid_pos in row:
                            grid_pos.clear()
                    break

                best_pos.get_active_neighbors()

                best_pos.open = "closed"

                open_positions = set(
                    [grid_pos for row in self.grid.get_grid() for grid_pos in row if grid_pos.open == "open"])

            '''for neighbor in start_point.get_active_neighbors():
                print(neighbor.solve_path, neighbor.f_cost,
                      neighbor.g_cost, neighbor.h_cost)

            self.solve = False'''

    # Renders visuals that are not important to the functionality of the program
    def draw_visuals(self):
        for row in self.grid.get_grid():
            for grid_pos in row:
                pygame.draw.rect(self.WIN, DARK_GREY,
                                 grid_pos.square_border, 1)

    def draw_core(self):  # Renders important display eliments
        for row in self.grid.get_grid():
            for grid_pos in row:
                if grid_pos.state == "null":
                    pygame.draw.rect(self.WIN, BLACK, grid_pos.square)
                elif grid_pos.state == "wall":
                    pygame.draw.rect(self.WIN, WHITE, grid_pos.square)
                elif grid_pos.state == "start":
                    pygame.draw.rect(self.WIN, GREEN, grid_pos.square)
                elif grid_pos.state == "end":
                    pygame.draw.rect(self.WIN, RED, grid_pos.square)

        try:
            for position in self.solution:
                if position.state != "start" and position.state != "end" and position.state != "wall":
                    pygame.draw.rect(self.WIN, BLUE, position.square)

        except Exception:
            pass

    def adjust_window(self, size: tuple):  # size: (width, height) # Resizes the window
        self.width, self.height = size

        pygame.display.set_mode(size)


start_point, end_point = (take_input())
test = Window((WIDTH, HEIGHT), start_point, end_point)
test.main()
