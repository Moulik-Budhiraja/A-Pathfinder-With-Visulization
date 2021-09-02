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


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)


class GridPos:
    def __repr__(self):
        return f'({self.x}, {self.y})'  # (x, y)

    # position: (x, y) #  dimensions: (width, height)
    def __init__(self, position: tuple, dimensions: tuple):
        self.x, self.y = position
        self.width, self.height = dimensions

        self.state = "null"


class Grid:
    def __init__(self, window, dimensions: tuple):  # dimensions: (width, height)
        self.width, self.height = dimensions
        self.window_width = WIDTH
        self.window_height = HEIGHT

        self.last_changed = (-1, -1)
        self.draw_mode = "add"

        self.window = window

        self.clean_window()
        self.generate_grid()
        self.assign_positions()

    def generate_grid(self):
        self.grid = []

        for y in range(self.height - 1, -1, -1):
            current_row = []
            for x in range(self.width):
                current_row.append(
                    GridPos((x, y), (self.box_width, self.box_height)))
            self.grid.append(current_row)

    def clean_window(self):
        self.box_width = self.window_width // self.width
        self.box_height = self.window_height // self.height

        new_window_width = self.box_width * self.width
        new_window_height = self.box_height * self.height

        self.window.adjust_window((new_window_width, new_window_height))

    def assign_positions(self):
        for row in self.grid:
            for grid_pos in row:
                x_pos = grid_pos.x * grid_pos.width
                y_pos = grid_pos.y * grid_pos.height
                grid_pos.square = pygame.Rect(
                    x_pos, y_pos, grid_pos.width, grid_pos.height)
                grid_pos.square_border = pygame.Rect(
                    x_pos, y_pos, grid_pos.width, grid_pos.height)

    def get_grid(self):
        return self.grid


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.WIN = pygame.display.set_mode((width, height))
        pygame.display.set_caption("A* Pathfinding")

        self.grid = Grid(self, (30, 30))  # ! Change to variables

    def main(self):
        self.mouse_down = False

        self.run = True
        while self.run:
            self.logic()

            self.WIN.fill((0, 0, 0))

            self.draw_core()
            self.draw_visuals()
            pygame.display.update()

    def logic(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:    # Removes all walls from grid
                    for row in self.grid.get_grid():
                        for grid_pos in row:
                            if grid_pos.state == "wall":
                                grid_pos.state = "null"

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True  # Stores left mouse button state

                for row in self.grid.get_grid():  # Loop through all positions to check which square was clicked
                    for grid_pos in row:
                        if grid_pos.square.collidepoint(event.pos):
                            if grid_pos.state == "null":
                                self.grid.draw_mode = "add"
                            elif grid_pos.state == "wall":
                                self.grid.draw_mode = "subtract"
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False

        if self.mouse_down:
            for row in self.grid.get_grid():
                for grid_pos in row:
                    if grid_pos.square.collidepoint(pygame.mouse.get_pos()):
                        if self.grid.last_changed != (grid_pos.x, grid_pos.y):
                            self.grid.last_changed = (grid_pos.x, grid_pos.y)

                            if self.grid.draw_mode == "add":
                                if grid_pos.state == "null":
                                    grid_pos.state = "wall"

                            elif self.grid.draw_mode == "subtract":
                                if grid_pos.state == "wall":
                                    grid_pos.state = "null"

    def draw_visuals(self):
        for row in self.grid.get_grid():
            for grid_pos in row:
                pygame.draw.rect(self.WIN, DARK_GREY,
                                 grid_pos.square_border, 1)

    def draw_core(self):
        for row in self.grid.get_grid():
            for grid_pos in row:
                if grid_pos.state == "null":
                    pygame.draw.rect(self.WIN, BLACK, grid_pos.square)
                elif grid_pos.state == "wall":
                    pygame.draw.rect(self.WIN, WHITE, grid_pos.square)

    def adjust_window(self, size: tuple):  # size: (width, height)
        self.width, self.height = size

        pygame.display.set_mode(size)


'''if __name__ == '__main__':
    test = Grid(30, 30)
    test.generate_grid()
    for i in test.grid:
        print(i)'''

take_input()
test = Window(WIDTH, HEIGHT)
test.main()


'''try:
    take_input()
    Window()
except Exception as e:
    print("Program closed unexpectedly")
    print(e)
'''
