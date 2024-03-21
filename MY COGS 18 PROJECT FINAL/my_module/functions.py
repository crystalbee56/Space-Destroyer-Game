import pygame
import random
import sys
import math

class SpaceDestroy:
    # Class variables

    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    PINK = (255, 192, 203)
    PURPLE = (198,42,214)
    GREY = (105,105,105)
    AQUA = (0,204,255)


    PLAYER_WIDTH = 50
    PLAYER_HEIGHT = 50
    PLAYER_SPEED = 5
    PLAYER_COLOR = WHITE

    OBSTACLE_SIZE = 50
    OBSTACLE_SPEED = 2
    OBSTACLE_COLORS = [PINK, BLUE, GREEN, PURPLE, GREY, AQUA]

    BULLET_WIDTH = 5
    BULLET_HEIGHT = 15
    BULLET_SPEED = 7
    BULLET_COLOR = RED

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Create the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Crystal's Space Destroyers")

        # Clock for controlling FPS
        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Add player to sprite group
        self.player = self.Player()
        self.all_sprites.add(self.player)

        # Add obstacles to sprite group
        self.spawn_obstacles()

        # Score variable
        self.score = 0

        # Font for displaying score
        self.font = pygame.font.Font(None, 36)

    def spawn_obstacles(self):
        for _ in range(8):
            obstacle = self.Obstacle()
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)

    def restart_game(self):
        self.all_sprites.empty()
        self.obstacles.empty()
        self.bullets.empty()
        self.player = self.Player()
        self.all_sprites.add(self.player)
        self.spawn_obstacles()
        

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = self.create_triangle(SpaceDestroy.PLAYER_WIDTH, SpaceDestroy.PLAYER_HEIGHT, SpaceDestroy.WHITE)
            self.rect = self.image.get_rect()
            self.rect.centerx = SpaceDestroy.SCREEN_WIDTH // 2
            self.rect.bottom = SpaceDestroy.SCREEN_HEIGHT - 10
            self.speed = SpaceDestroy.PLAYER_SPEED

        def create_triangle(self, width, height, color):
            triangle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            points = [(0, height), (width // 2, 0), (width, height)]
            pygame.draw.polygon(triangle_surface, color, points)
            return triangle_surface

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            self.check_boundary()

        def check_boundary(self):
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SpaceDestroy.SCREEN_WIDTH:
                self.rect.right = SpaceDestroy.SCREEN_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > SpaceDestroy.SCREEN_HEIGHT:
                self.rect.bottom = SpaceDestroy.SCREEN_HEIGHT

    # Obstacle class
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.color = random.choice(SpaceDestroy.OBSTACLE_COLORS)
            self.image = self.create_star(SpaceDestroy.OBSTACLE_SIZE, self.color)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(SpaceDestroy.SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(SpaceDestroy.OBSTACLE_SPEED // 2, SpaceDestroy.OBSTACLE_SPEED)

        def create_star(self, size, color):
            inner_radius = size // 3
            outer_radius = size // 2
            num_points = 5
            points = []
            for i in range(2 * num_points):
                radius = outer_radius if i % 2 == 0 else inner_radius
                angle = math.radians(i * 360 / (2 * num_points))
                x = size // 2 + radius * math.cos(angle)
                y = size // 2 + radius * math.sin(angle)
                points.append((x, y))
            star_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.polygon(star_surface, color, points)
            return star_surface

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > SpaceDestroy.SCREEN_HEIGHT + 10:
                self.rect.x = random.randrange(SpaceDestroy.SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(SpaceDestroy.OBSTACLE_SPEED // 2, SpaceDestroy.OBSTACLE_SPEED)

    # Bullet class
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((SpaceDestroy.BULLET_WIDTH, SpaceDestroy.BULLET_HEIGHT))
            self.image.fill(SpaceDestroy.BULLET_COLOR)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -SpaceDestroy.BULLET_SPEED

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()
                


    def run(self):
        # Game loop
        running = True
        while running:
            # Keep loop running at the right speed
            self.clock.tick(60)

            # Process input (events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        bullet = self.Bullet(self.player.rect.centerx, self.player.rect.top)
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)

            # Update
            self.all_sprites.update()

            # Check for collisions
            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if hits:
                self.restart_game()
                self.score = 0  # Reset score

            hits = pygame.sprite.groupcollide(self.obstacles, self.bullets, True, True)
            for hit in hits:
                obstacle = self.Obstacle()
                self.all_sprites.add(obstacle)
                self.obstacles.add(obstacle)
                self.score += 30  
            
            #Clear the screen
            self.screen.fill(self.BLACK)

            # Display the scoreboard at the top of the screen
            score_text = f"Score: {self.score}"  # Format the score text
            score_surface = self.font.render(score_text, True, self.WHITE)  # Render the score text
            score_rect = score_surface.get_rect(topright=(self.SCREEN_WIDTH - 20, 20))  # Get the score text rectangle
            self.screen.blit(score_surface, score_rect)

            # Draw / render
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
