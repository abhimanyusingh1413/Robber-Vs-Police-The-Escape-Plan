
import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load('selection.png').convert_alpha()
        self.checkpoints = []  # Store checkpoints
        self.robber = pygame.sprite.GroupSingle(robber(self.empty_path, self.checkpoints))
        self.police = pygame.sprite.Group([
            Police(self.robber, matrix, (600, 600)),
            Police(self.robber, matrix, (200, 200)),
            Police(self.robber, matrix, (1000, 500))
        ])
        self.start_time = pygame.time.get_ticks()
        self.time_left = 30  # Countdown timer set to 30 seconds
        self.game_over = False
        self.font = pygame.font.Font(None, 50)

    def empty_path(self):
        self.checkpoints.clear()

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row, col = mouse_pos[1] // 32, mouse_pos[0] // 32
        if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]) and self.matrix[row][col] == 1:
            rect = pygame.Rect((col * 32, row * 32), (32, 32))
            screen.blit(self.select_surf, rect)

    def create_path(self):
        if not self.game_over:
            mouse_pos = pygame.mouse.get_pos()
            target_x, target_y = mouse_pos[0] // 32, mouse_pos[1] // 32
            if self.matrix[target_y][target_x] == 1:  # Prevent selecting obstacles
                self.checkpoints.append((target_x, target_y))
                self.robber.sprite.update_path()

    def draw_path(self):
        for point in self.checkpoints:
            pygame.draw.circle(screen, 'blue', (point[0] * 32 + 16, point[1] * 32 + 16), 6)

    def update_timer(self):
        if not self.game_over:
            self.time_left = max(30 - (pygame.time.get_ticks() - self.start_time) // 1000, 0)

    def check_game_over(self):
        robber_pos = self.robber.sprite.get_coord()
        for police in self.police:
            if police.get_coord() == robber_pos:
                self.game_over = True
                return "YOU LOST! \n \n Caught by police!"

        if self.time_left == 0:  # Win condition
            self.game_over = True
            return " YOU WON! \n \n Survived 30 seconds!"

        return None

   
    def draw_score_and_message(self):
        timer_text = self.font.render(f"Time left: {self.time_left}", True, (0, 0, 0))
        screen.blit(timer_text, (20, 20))

        message = self.check_game_over()
        if message:
            message_lines = message.split("\n")  # Split message into lines
            y_offset = 350  # Starting y position for message
            for line in message_lines:
                text_surf = self.font.render(line, True, (0, 0, 255))  # Blue color (RGB)
                text_rect = text_surf.get_rect(center=(640, y_offset))
                screen.blit(text_surf, text_rect)
                y_offset += 50  # Move down for the next line

    def update(self):
        if not self.game_over:
            self.update_timer()
            self.draw_active_cell()
            self.draw_path()
            self.robber.update()
            self.police.update()

        self.robber.draw(screen)
        self.police.draw(screen)
        self.draw_score_and_message()


class robber(pygame.sprite.Sprite):
    def __init__(self, empty_path, checkpoints):
        super().__init__()
        self.image = pygame.image.load('robber.png').convert_alpha()
        self.rect = self.image.get_rect(center=(60, 60))
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 3
        self.direction = pygame.Vector2(0, 0)
        self.checkpoints = checkpoints
        self.empty_path = empty_path

    def get_coord(self):
        return self.rect.centerx // 32, self.rect.centery // 32

    def update_path(self):
        if self.checkpoints:
            next_checkpoint = self.checkpoints[0]
            next_pos = pygame.Vector2(next_checkpoint[0] * 32 + 16, next_checkpoint[1] * 32 + 16)
            self.direction = (next_pos - self.pos).normalize()

    def check_collisions(self):
        if self.checkpoints and pygame.Vector2(self.checkpoints[0][0] * 32 + 16, self.checkpoints[0][1] * 32 + 16).distance_to(self.pos) < 5:
            self.checkpoints.pop(0)
            if self.checkpoints:
                self.update_path()
            else:
                self.empty_path()

    def update(self):
        if self.checkpoints:
            self.pos += self.direction * self.speed
            self.check_collisions()
        self.rect.center = self.pos


class Police(pygame.sprite.Sprite):
    def __init__(self, target, matrix, start_pos):
        super().__init__()
        self.image = pygame.image.load('police.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.Vector2(start_pos)
        self.speed = 1.5  # Reduced speed for balance
        self.direction = pygame.Vector2(0, 0)
        self.target = target
        self.matrix = matrix
        self.path = []
        self.last_target_position = None

    def get_coord(self):
        return self.rect.centerx // 32, self.rect.centery // 32

    def find_path(self):
        if not self.target.sprite.checkpoints:
            return

        target_position = self.target.sprite.checkpoints[0]
        if self.last_target_position == target_position:
            return

        self.last_target_position = target_position
        grid = Grid(matrix=self.matrix)

        start_x, start_y = self.get_coord()
        start = grid.node(start_x, start_y)

        end_x, end_y = target_position
        if self.matrix[end_y][end_x] == 0:  # Ensure police don't target obstacles
            return

        end = grid.node(end_x, end_y)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)  # No diagonal movement
        self.path, _ = finder.find_path(start, end, grid)

        grid.cleanup()
        self.get_direction()

    def get_direction(self):
        if self.path:
            next_pos = pygame.Vector2(self.path[0].x * 32 + 16, self.path[0].y * 32 + 16)
            self.direction = (next_pos - self.pos).normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

    def check_collisions(self):
        if self.path and pygame.Vector2(self.path[0].x * 32 + 16, self.path[0].y * 32 + 16).distance_to(self.pos) < 3:
            self.path.pop(0)
            self.get_direction()

    def update(self):
        self.find_path()
        if self.path:
            self.pos += self.direction * self.speed
            self.check_collisions()
        self.rect.center = self.pos


pygame.init()
screen = pygame.display.set_mode((1280, 736))
clock = pygame.time.Clock()
bg_surf = pygame.image.load('map.png').convert()
matrix = [[1 if x == 1 else 0 for x in row] for row in [[1] * 40] * 23]
pathfinder = Pathfinder(matrix)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()

    screen.blit(bg_surf, (0, 0))
    pathfinder.update()
    pygame.display.update()
    clock.tick(60)

