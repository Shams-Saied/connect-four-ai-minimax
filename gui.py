import pygame
import sys
from connect4 import Game
import algorithms

# Constants
COLS = 7
ROWS = 6
CELL_SIZE = 100
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
RADIUS = CELL_SIZE // 2 - 5

# Window dimensions
TOP_MARGIN = 80
BOTTOM_MARGIN = 100
WINDOW_WIDTH = BOARD_WIDTH
WINDOW_HEIGHT = TOP_MARGIN + BOARD_HEIGHT + BOTTOM_MARGIN

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
BLACK = (0, 0, 0)
RED = (230, 50, 50)
DARK_RED = (210, 30, 30)
YELLOW = (255, 200, 40)
DARK_YELLOW = (235, 180, 20)
DARK_GRAY = (80, 80, 80)
LIGHT_BLUE = (188, 214, 228)
SKY_BLUE = (120, 193, 229)
DARK_BLUE = (0, 80, 160)
ORANGE = (255, 140, 50)

class RoundedButton:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.border_radius = 12
    
    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=self.border_radius)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
    
    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Connect4GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect 4")
        self.clock = pygame.time.Clock()
        self.status_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.board_x = (WINDOW_WIDTH - BOARD_WIDTH) // 2
        self.board_y = TOP_MARGIN
        button_width = 110
        button_height = 45
        button_y = self.board_y + BOARD_HEIGHT + 20
        start_x = (WINDOW_WIDTH - (button_width * 4 + 150)) // 2
        
        self.buttons = {
            "reset": RoundedButton(start_x, button_y, button_width, button_height, "Reset", BLUE, DARK_GRAY, BLACK),
            "minimax": RoundedButton(start_x + button_width + 10, button_y, button_width, button_height, "Minimax", LIGHT_BLUE, SKY_BLUE, BLACK),
            "alphabeta": RoundedButton(start_x + (button_width + 10) * 2, button_y, button_width, button_height, "Alpha-Beta", LIGHT_BLUE, SKY_BLUE, BLACK),
            "expectimax": RoundedButton(start_x + (button_width + 10) * 3, button_y, button_width, button_height, "Expectimax", LIGHT_BLUE, SKY_BLUE, BLACK),
        }
        
        self.depth_input = ""
        self.depth_active = False
        self.depth_rect = pygame.Rect(WINDOW_WIDTH - 130, button_y, 80, button_height)
        
        self.game = Game(COLS, ROWS)
        self.current_algorithm = "minimax"
        self.current_depth = 3
        self.reset_counters()
    
    def reset_counters(self):
        algorithms.minimax_node_count = 0
        algorithms.node_count = 0
        algorithms.expectimax_node_count =0
    
    def board_to_2d_list(self):
        return [row[:] for row in self.game.board.board]
    
    def draw_board(self):
        board_rect = pygame.Rect(self.board_x, self.board_y, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.screen, BLUE, board_rect)
        pygame.draw.rect(self.screen, DARK_BLUE, board_rect, 3)
        
        for row in range(ROWS):
            for col in range(COLS):
                center_x = self.board_x + col * CELL_SIZE + CELL_SIZE // 2
                center_y = self.board_y + row * CELL_SIZE + CELL_SIZE // 2
                piece = self.game.board.board[row][col]
                color = WHITE
                pygame.draw.circle(self.screen, BLACK, (center_x, center_y), RADIUS + 2)
                pygame.draw.circle(self.screen, color, (center_x, center_y), RADIUS)
                if piece == 1:
                    pygame.draw.circle(self.screen, RED, (center_x, center_y), RADIUS)
                    pygame.draw.circle(self.screen, DARK_RED, (center_x, center_y), RADIUS - 6)
                    pygame.draw.circle(self.screen, RED, (center_x, center_y), RADIUS - 10)
                elif piece == 2:
                    pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), RADIUS)
                    pygame.draw.circle(self.screen, DARK_YELLOW, (center_x, center_y), RADIUS - 6)
                    pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), RADIUS - 10)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.game.game_over and self.game.current_player == 1:
            if (self.board_x <= mouse_x <= self.board_x + BOARD_WIDTH and
                self.board_y <= mouse_y <= self.board_y + BOARD_HEIGHT):
                col = (mouse_x - self.board_x) // CELL_SIZE
                if 0 <= col < COLS and self.game.board.is_valid_column(col):
                    hover_rect = pygame.Rect(
                        self.board_x + col * CELL_SIZE,
                        self.board_y,
                        CELL_SIZE,
                        BOARD_HEIGHT
                    )
                    hover_surface = pygame.Surface((CELL_SIZE, BOARD_HEIGHT))
                    hover_surface.set_alpha(80)
                    hover_surface.fill((255, 255, 255))
                    self.screen.blit(hover_surface, hover_rect.topleft)
                    preview_y = self.board_y - 30
                    pygame.draw.circle(self.screen, RED, (self.board_x + col * CELL_SIZE + CELL_SIZE // 2, preview_y), RADIUS // 2)
    
    def draw_top_status(self):
        if self.game.game_over:
            human_score, ai_score = self.game.board.get_scores()
            if self.game.draw:
                status_text = f"Game Over - Tie! ({human_score} - {ai_score})"
                status_color = ORANGE
            elif self.game.winner == 1:
                status_text = f"Game Over - Human Wins! ({human_score} - {ai_score})"
                status_color = RED
            else:
                status_text = f"Game Over - AI Wins! ({human_score} - {ai_score})"
                status_color = YELLOW
        else:
            human_score, ai_score = self.game.board.get_scores()
            if self.game.current_player == 1:
                status_text = f"Your Turn (Red)  |  Scores: You {human_score} - {ai_score} AI"
                status_color = RED
            else:
                status_text = f"AI Turn (Yellow)  |  Scores: You {human_score} - {ai_score} AI"
                status_color = YELLOW
        
        status_bg = pygame.Rect(0, 10, WINDOW_WIDTH, 50)
        pygame.draw.rect(self.screen, WHITE, status_bg)
        
        status_surface = self.status_font.render(status_text, True, status_color)
        status_x = (WINDOW_WIDTH - status_surface.get_width()) // 2
        self.screen.blit(status_surface, (status_x, 20))
        
        algo_text = f"Algorithm: {self.current_algorithm.upper()}  |  Search Depth (K): {self.current_depth}"
        algo_surface = self.small_font.render(algo_text, True, DARK_GRAY)
        algo_x = (WINDOW_WIDTH - algo_surface.get_width()) // 2
        self.screen.blit(algo_surface, (algo_x, 55))
        
        pygame.draw.line(self.screen, LIGHT_BLUE, (50, 78), (WINDOW_WIDTH - 50, 78), 2)
    
    def draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons.values():
            button.update_hover(mouse_pos)
            button.draw(self.screen, self.small_font)
        
        if self.current_algorithm == "minimax":
            self.buttons["minimax"].color = SKY_BLUE
            self.buttons["minimax"].hover_color = BLUE
            self.buttons["alphabeta"].color = LIGHT_BLUE
            self.buttons["expectimax"].color = LIGHT_BLUE
        elif self.current_algorithm == "alphabeta":
            self.buttons["alphabeta"].color = SKY_BLUE
            self.buttons["alphabeta"].hover_color = BLUE
            self.buttons["minimax"].color = LIGHT_BLUE
            self.buttons["expectimax"].color = LIGHT_BLUE
        elif self.current_algorithm == "expectimax":
            self.buttons["expectimax"].color = SKY_BLUE
            self.buttons["expectimax"].hover_color = BLUE
            self.buttons["minimax"].color = LIGHT_BLUE
            self.buttons["alphabeta"].color = LIGHT_BLUE
        
        color = SKY_BLUE if self.depth_active else DARK_GRAY
        pygame.draw.rect(self.screen, WHITE, self.depth_rect, border_radius=8)
        pygame.draw.rect(self.screen, color, self.depth_rect, 2, border_radius=8)
        
        depth_label = self.small_font.render(str(self.current_depth), True, BLACK)
        label_x = self.depth_rect.x + (self.depth_rect.width - depth_label.get_width()) // 2
        label_y = self.depth_rect.y + (self.depth_rect.height - depth_label.get_height()) // 2
        self.screen.blit(depth_label, (label_x, label_y))
        
        k_label = self.small_font.render("K =", True, DARK_GRAY)
        self.screen.blit(k_label, (self.depth_rect.x - 35, self.depth_rect.y + 12))
        
        if self.depth_active:
            instruction = self.small_font.render("Enter depth (1-5) and press ENTER", True, DARK_GRAY)
            inst_x = self.depth_rect.x - 100
            inst_y = self.depth_rect.y - 25
            self.screen.blit(instruction, (inst_x, inst_y))
    
    def handle_click(self, pos):
        x, y = pos
        
        if self.buttons["reset"].click(pos):
            self.game.reset_game()
            return True
        
        if self.buttons["minimax"].click(pos):
            self.current_algorithm = "minimax"
            self.game.ai_algorithm = "minimax"
            return True
        
        if self.buttons["alphabeta"].click(pos):
            self.current_algorithm = "alphabeta"
            self.game.ai_algorithm = "alphabeta"
            return True
        
        if self.buttons["expectimax"].click(pos):
            self.current_algorithm = "expectimax"
            self.game.ai_algorithm = "expectimax"
            return True
        
        if self.depth_rect.collidepoint(x, y):
            self.depth_active = True
            self.depth_input = ""
            return True
        else:
            self.depth_active = False
        
        if not self.game.game_over and self.game.current_player == 1:
            if (self.board_x <= x <= self.board_x + BOARD_WIDTH and
                self.board_y <= y <= self.board_y + BOARD_HEIGHT):
                col = (x - self.board_x) // CELL_SIZE
                if 0 <= col < COLS:
                    if self.game.make_move(col):
                        pygame.display.flip()
                        # After human move, print heuristic values
                        board_2d = self.board_to_2d_list()
                        algorithms.print_board_heuristic(board_2d)
                        return True
        return False
    
    def handle_keyboard(self, event):
        if self.depth_active:
            if event.key == pygame.K_RETURN:
                if self.depth_input.isdigit():
                    depth_val = int(self.depth_input)
                    if 1 <= depth_val <= 10:
                        self.current_depth = depth_val
                        self.game.search_depth = self.current_depth
                self.depth_input = ""
                self.depth_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.depth_input = self.depth_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.depth_active = False
                self.depth_input = ""
            else:
                if event.unicode.isdigit() and len(self.depth_input) < 2:
                    self.depth_input += event.unicode
    
    def ai_move(self):
        if self.game.game_over or self.game.current_player != 2:
            return False
        
        board_2d = self.board_to_2d_list()
        depth = self.current_depth
        col = None
        # Call the appropriate algorithm and reset node counters
        try:
            if self.current_algorithm == "minimax":
                algorithms.minimax_node_count = 0
                col, _ = algorithms.minimax(board_2d, depth, True)
            elif self.current_algorithm == "alphabeta":
                algorithms.node_count = 0
                col, _ = algorithms.alpha_beta(board_2d, depth, -float('inf'), float('inf'), True)
            elif self.current_algorithm == "expectimax":
                algorithms.expectimax_node_count = 0
                col, _ = algorithms.expectimax(board_2d, depth, True)
        except Exception as e:
            print(f"Error in AI algorithm: {e}")
            
        if col is not None and self.game.make_move(col):
            # heuristic display
            board_2d = self.board_to_2d_list()
            algorithms.print_board_heuristic(board_2d)
            return True
        return False
        
        
    def run(self):
        running = True
        ai_thinking = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard(event)
            
            # AI move
            if not self.game.game_over and self.game.current_player == 2 and not ai_thinking:
                ai_thinking = True
                self.ai_move()
                ai_thinking = False
            
            self.screen.fill(WHITE)
            self.draw_top_status()
            self.draw_board()
            self.draw_buttons()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = Connect4GUI()
    gui.run()

