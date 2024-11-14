import random
import pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length=9, removed_cells=40):
        self.row_length = row_length
        self.board = [[0] * row_length for _ in range(row_length)]
        self.removed_cells = removed_cells

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return [row[:] for row in self.board]

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    '''
    Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(self.row_length))

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                num = numbers.pop()
                self.board[row_start + i][col_start + j] = num

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if row == 9:
            return True
        if col == 9:
            return self.fill_remaining(row + 1, 0)
        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        if not self.fill_remaining(0, 0):
            raise Exception("Failed to fill the Sudoku board.")

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        count = 0
        while count < self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.fill_values()
    generator.remove_cells()
    return generator.get_board()


class Cell:
    def __init__(self, value, row, col, screen, font):
        self.value = value
        self.initial_value = value
        self.correct = value
        self.sketch = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.font = font
        self.selected = False

    def draw(self):
        x = self.col * 50 + 10
        y = self.row * 50 + 10
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, 40, 40))
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40), 2)

        text = str(self.value) if self.value != 0 else str(self.sketch) if self.sketch != 0 else ''
        text_color = (0, 0, 0) if self.value != 0 else (128, 128, 128)
        if text:
            text_surface = self.font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=(x + 20, y + 20))
            self.screen.blit(text_surface, text_rect)

    def set_value(self, value):
        if self.correct == 0:
            self.value = value

    def set_sketched_value(self, value):

        if self.value == 0:
            self.sketch = value

    def confirm_cell_value(self):
        if self.sketch != 0 and self.value == 0:
            self.value = self.sketch
            self.sketch = 0

    def reset(self):
        self.value = self.initial_value
        self.sketch = 0


class Board:
    def __init__(self, screen, font, puzzle):
        self.screen = screen
        self.font = font
        self.cells = []
        self.selected_cell = None
        self.load_puzzle(puzzle)

    def confirm_cell_value(self):
        if self.selected_cell and self.selected_cell.sketch != 0:
            self.selected_cell.set_value(self.selected_cell.sketch)
            self.selected_cell.sketch = 0

    def load_puzzle(self, puzzle):
        self.cells = [[Cell(puzzle[i][j], i, j, self.screen, self.font) for j in range(9)] for i in range(9)]

    def draw(self):
        self.screen.fill((255, 255, 255))
        for row in self.cells:
            for cell in row:
                cell.draw()
        for i in range(0, 10, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 50 + 10, 10), (i * 50 + 10, 460), 4)
            pygame.draw.line(self.screen, (0, 0, 0), (10, i * 50 + 10), (460, i * 50 + 10), 4)

    def navigate(self, direction):
        if not self.selected_cell:
            return
        row, col = self.selected_cell.row, self.selected_cell.col
        mapping = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        new_row, new_col = row + mapping[direction][0], col + mapping[direction][1]
        if 0 <= new_row < 9 and 0 <= new_col < 9:
            self.select_cell(new_row, new_col)

    def select_cell(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def set_cell_value(self, value):
        if self.selected_cell and self.selected_cell.correct == 0:
            self.selected_cell.set_value(value)

    def confirm_cell_value(self):
        if self.selected_cell:
            self.selected_cell.confirm_cell_value()

    def check_win(self):
        for group in (self.cells, zip(*self.cells)):
            for line in group:
                if not self.is_complete([cell.value for cell in line]):
                    return False
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                box = [self.cells[x + dx][y + dy].value for dx in range(3) for dy in range(3)]
                if not self.is_complete(box):
                    return False
        return True

    def is_complete(self, values):
        return sorted(values) == list(range(1, 10))

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                cell.reset()


def draw_button(screen, text, position, width, height, font, color=(255, 150, 0), text_color=(255, 255, 255)):
    button_rect = pygame.Rect(position[0], position[1], width, height)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(position[0] + width // 2, position[1] + height // 2))
    screen.blit(text_surf, text_rect)
    return button_rect


def manage_buttons(screen, font):
    screen_width = screen.get_width()
    button_width = 120
    button_height = 50
    button_spacing = 20
    total_width = 3 * button_width + 2 * button_spacing
    start_x = (screen_width - total_width) // 2
    y_position = screen.get_height() - button_height - 30

    reset_button = draw_button(screen, "Reset", (start_x, y_position), button_width, button_height, font,
                               color=(0, 0, 255), text_color=(255, 255, 255))
    restart_button = draw_button(screen, "Restart", (start_x + button_width + button_spacing, y_position), button_width,
                                 button_height, font, color=(0, 255, 0), text_color=(255, 255, 255))
    exit_button = draw_button(screen, "Quit", (start_x + 2 * (button_width + button_spacing), y_position), button_width,
                              button_height, font, color=(255, 0, 0), text_color=(255, 255, 255))

    return reset_button, restart_button, exit_button


def show_game_over(screen, font):
    screen.fill((0, 0, 0))
    font_large = pygame.font.Font(None, 72)
    text = font_large.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(225, 150))
    screen.blit(text, text_rect)

    quit_button = draw_button(screen, "Quit", (150, 350), 150, 50, font, color=(255, 0, 0), text_color=(255, 255, 255))
    restart_button = draw_button(screen, "Restart", (150, 250), 150, 50, font, color=(0, 255, 0),
                                 text_color=(255, 255, 255))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if quit_button.collidepoint(x, y):
                    pygame.quit()
                    return False
                elif restart_button.collidepoint(x, y):
                    return True

    return False


def main_menu(screen, font):
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))

    welcome_font = pygame.font.Font(None, 50)
    welcome_message = "Welcome to Sudoku"
    welcome_text = welcome_font.render(welcome_message, True, (0, 0, 255))
    welcome_rect = welcome_text.get_rect(center=(225, 100))
    screen.blit(welcome_text, welcome_rect)

    buttons = {
        'easy': (150, 200),
        'medium': (150, 275),
        'hard': (150, 350)
    }
    button_objects = {}
    for label, pos in buttons.items():
        button_objects[label] = draw_button(screen, label.capitalize(), pos, 150, 50, font)

    pygame.display.flip()

    running = True
    selected_difficulty = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for difficulty, button in button_objects.items():
                    if button.collidepoint(x, y):
                        selected_difficulty = difficulty
                        running = False
                        break

        clock.tick(30)
    return selected_difficulty


def show_game_won(screen, font):
    screen.fill((0, 0, 255))
    font_large = pygame.font.Font(None, 72)
    text = font_large.render("You Win!", True, (255, 150, 0))
    text_rect = text.get_rect(center=(225, 225))
    screen.blit(text, text_rect)

    quit_button = draw_button(screen, "Quit", (150, 300), 150, 50, font, color=(255, 0, 0), text_color=(255, 255, 255))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return False
    return True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return 'quit'
                if restart_button.collidepoint(event.pos):
                    return 'restart'
    return 'quit'