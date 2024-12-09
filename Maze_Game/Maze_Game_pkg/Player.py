import pygame
import time as t
from Maze_Game_pkg.Exceptions import *

class Player:
    def __init__(self, tile_num, player_image, screen):
        self.tile_num    = tile_num
        self.image       = player_image
        self.screen       = screen
        self.first_move   = t.time()
        self.passed_checkpoint = False

    def cal_next_tile_num(self, user_key, maze):
        if user_key == 'UP':
            change = -maze.width
        elif user_key == 'DOWN':
            change = maze.width
        elif user_key == 'LEFT':
            change = -1
        elif user_key == 'RIGHT':
            change = 1
        else:
            raise ValueError("잘못된 키 입력")
        return self.tile_num + change


    def move_player(self, user_key, maze):
        next_tile_num = self.cal_next_tile_num(user_key, maze)
        if next_tile_num == maze.exit_tile_num and maze.now_map_data[next_tile_num] == 0:
            raise CheckpointNotPassedError('CheckPoint Disabled !')
        
        if maze.now_map_data[next_tile_num] == 1:
            
            if next_tile_num == maze.check_point_tile_num:
                if self.passed_checkpoint:
                    None
                else:
                    pygame.mixer.Sound('Maze_Game_pkg/Data_Sets/activated_checkpoint.wav').play()
                    self.passed_checkpoint = True
                    
            self.tile_num = next_tile_num
            pygame.mixer.Sound('Maze_Game_pkg/Data_Sets/player_moving_sound.mp3').play()
            return True
        else:
            raise MoveToWallError
            return False


    def show_player(self, maze):
        x, y = maze.coords[self.tile_num]
        self.screen.blit(self.image, (x, y))

    def is_moving_too_fast(self):
        second_move = t.time()
        if second_move - self.first_move < 0.1:
            return True
        else:
            self.first_move = second_move
            return False

    def is_stuck_in_wall(self, maze):
        if  maze.now_map_data[ self.tile_num ] == 0:
            self.tile_num = maze.width + 1
