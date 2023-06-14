import pygame
import os
import time
import random

from model.Crossing import cross
from model.Enemy import Enemy
from model.LevelEnemies import AllEnemies
from model.Player import Player
from model.Ship import AllShips
from view.viewgame import ViewGame


class Game:
    def __init__(self):
        self.run = True
        self.FPS = 60
        self.level = 1
        self.lives = 5
        self.scores = 0
        self.lost_count = 0
        self.lost = False
        self.player_speed = 4
        self.laser_speed = 5

        self.view_of_game = ViewGame()

    def main_menu(self):
        pygame.mixer_music.stop()
        self.run = True
        self.level = 1
        self.lives = 5
        self.scores = 0
        self.lost_count = 0
        self.lost = False
        self.view_of_game.ship = Player(self.view_of_game.window.get_width() / 2 - 30,
                                        self.view_of_game.window.get_height() - 40, self.view_of_game.window,
                           self.view_of_game.YELLOW_MAIN_SHIP, self.view_of_game.YELLOW_LASER)
        while self.run:
            mouse = pygame.mouse.get_pos()
            self.view_of_game.redraw_window_menu()
            for event in pygame.event.get():
                self.view_of_game.redraw_window_menu()
                if event.type == pygame.QUIT:
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view_of_game.width/3 < mouse[0] < 2*self.view_of_game.width/3 and \
                            self.view_of_game.height/4 < mouse[1] < (self.view_of_game.height/4)\
                            + self.view_of_game.height/6:
                        self.view_of_game.sound_menu.play()
                        pygame.mixer_music.play(20)
                        self.main()
                    if self.view_of_game.width / 3 < mouse[0] < 2 * self.view_of_game.width / 3 and \
                           (self.view_of_game.height/4)+self.view_of_game.height/6 < mouse[1] \
                            < (self.view_of_game.height/4)+2*self.view_of_game.height/6:
                        self.view_of_game.sound_menu.play()
                        print("Table")
                    if self.view_of_game.width / 3 < mouse[0] < 2 * self.view_of_game.width / 3 and \
                            (self.view_of_game.height / 4) + 2 * self.view_of_game.height / 6 < mouse[1] \
                            < (self.view_of_game.height / 4) + 3 * self.view_of_game.height / 6:
                        self.view_of_game.sound_menu.play()
                        quit(0)
        pygame.quit()

    def main(self):

        main_ship = self.view_of_game.ship

        clock = pygame.time.Clock()
        all_level_enemies = AllEnemies(self.view_of_game, self.level)
        enemies = all_level_enemies.enemies
        while self.run:
            clock.tick(self.FPS)
            self.view_of_game.redraw_window(self.lives, self.level, enemies, self.lost, self.scores)
            if self.lost:
                if self.lost_count > self.FPS * 3:
                    self.run = False
                else:
                    self.lost_count += 1
                    continue
            if self.lives < 0 or main_ship.health <= 0:
                pygame.mixer_music.stop()
                self.view_of_game.sound_death.play()
                self.lost = True




            if len(enemies) == 0:
                self.level += 1
                enemies = all_level_enemies.make_level_enemies()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and main_ship.x - self.player_speed > 0:#ДВижение влево
                main_ship.x -= self.player_speed
            if keys[pygame.K_d] and main_ship.x < self.view_of_game.window.get_width() - 30:
                main_ship.x += self.player_speed
            if keys[pygame.K_w] and main_ship.y > 0:
                main_ship.y -= self.player_speed
            if keys[pygame.K_s] and main_ship.y < self.view_of_game.window.get_height() - 50:
                main_ship.y += self.player_speed
            if keys[pygame.K_SPACE]:
                self.view_of_game.sound_laser.play()
                main_ship.shoot()
            if keys[pygame.K_ESCAPE]:
                self.run =False
            for enemy in enemies:
                enemy.move()
                enemy.move_lasers(self.laser_speed, main_ship)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    self.scores += 10
                if random.randrange(0, 180) == 1:
                    enemy.shoot()
                if cross(enemy, main_ship):
                    self.scores += 10
                    main_ship.health -= 20
                    enemies.remove(enemy)

                elif enemy.y + enemy.get_height() > self.view_of_game.height:
                    self.lives -= 1
                    enemies.remove(enemy)

            main_ship.move_lasers(self.laser_speed, enemies)
        self.main_menu()