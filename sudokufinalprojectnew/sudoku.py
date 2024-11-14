from sudoku_generator import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((450, 550))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.Font(None, 40)

    running = True
    show_menu = True
    while running:
        if show_menu:
            difficulty = main_menu(screen, font)
            if difficulty is None:
                running = False
                continue

        game_reset = True
        while game_reset:
            game_reset = False
            screen.fill((200, 200, 200))
            pygame.display.flip()

            removed_cells = {'easy': 30, 'medium': 40, 'hard': 50}.get(difficulty, 40)
            puzzle = generate_sudoku(9, removed_cells)
            board = Board(screen, font, puzzle)
            board.draw()
            reset_button, restart_button, exit_button = manage_buttons(screen, font)

            game_running = True
            while game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if reset_button.collidepoint(x, y):
                            board.reset_to_original()
                        elif restart_button.collidepoint(x, y):
                            show_menu = True
                            game_running = False
                        elif exit_button.collidepoint(x, y):
                            pygame.quit()
                            return
                        else:
                            col, row = x // 50, y // 50
                            board.select_cell(row, col)

                    elif event.type == pygame.KEYDOWN:
                        handle_key_events(event, board, screen, font)

                if game_running:
                    screen.fill((200, 200, 200))
                    board.draw()
                    reset_button, restart_button, exit_button = manage_buttons(screen, font)
                    pygame.display.flip()

    pygame.quit()


def handle_key_events(event, board, screen, font):
    print(f"Key pressed: {pygame.key.name(event.key)}")
    if pygame.K_1 <= event.key <= pygame.K_9:
        value = int(chr(event.key))
        print(f"Sketching cell value: {value}")
        if board.selected_cell:
            board.selected_cell.set_sketched_value(value)
        board.draw()
        pygame.display.flip()

    elif event.key == pygame.K_RETURN:
        print("Confirming cell value.")
        if board.selected_cell:
            board.selected_cell.confirm_cell_value()
            board.draw()
            pygame.display.flip()

        if board.is_full():
            if board.check_win():
                print("Game Won")
                show_game_won(screen, font)
            else:
                print("Game Lost")
                show_game_over(screen, font)

    elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
        directions = {
            pygame.K_UP: 'up',
            pygame.K_DOWN: 'down',
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right'
        }
        direction = directions[event.key]
        print(f"Navigating: {direction}")
        board.navigate(direction)
        board.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()