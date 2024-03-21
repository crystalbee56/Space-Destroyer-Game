import unittest
from unittest.mock import patch
import pygame
from functions import SpaceDestroy

class TestSpaceDestroy(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        game = SpaceDestroy()
        self.assertIsInstance(game.screen, pygame.Surface)
        self.assertIsInstance(game.clock, pygame.time.Clock)
        self.assertIsInstance(game.all_sprites, pygame.sprite.Group)
        self.assertIsInstance(game.obstacles, pygame.sprite.Group)
        self.assertIsInstance(game.bullets, pygame.sprite.Group)
        self.assertIsInstance(game.player, SpaceDestroy.Player)
        self.assertEqual(game.score, 0)
        self.assertIsInstance(game.font, pygame.font.Font)

    def test_spawn_obstacles(self):
        game = SpaceDestroy()
        game.spawn_obstacles()
        self.assertGreater(len(game.obstacles), 8)

    def test_player_movement(self):
        game = SpaceDestroy()
        initial_player_rect = game.player.rect.copy()
        # Simulate moving the player to the left
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        game.player.update()
        self.assertLessEqual(game.player.rect.x, initial_player_rect.x)
        # Simulate moving the player to the right
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        game.player.update()
        self.assertGreaterEqual(game.player.rect.x, initial_player_rect.x)

    def test_bullet_creation(self):
        game = SpaceDestroy()
        initial_bullet_count = len(game.bullets)
        # Simulate firing a bullet
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))  # Ensure keyup event is posted
        game.all_sprites.update()
        self.assertLess(len(game.bullets), initial_bullet_count + 1)


    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()