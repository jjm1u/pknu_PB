import numpy as np
import random as rd
import pygame

class Maze:
    def __init__(self, width, height):
        self.width                     = width
        self.height                    = height
        self.mapsize                  = height * width
        self.map_data                = [self.generate_maze() for _ in range(3)]
        self.coords                    = [(x, y + 45) for y in range(0, self.height * 15, 15) for x in range(0, self.width * 15, 15)]
        self.exit_tile_num            = self.mapsize - self.width - 1
        self.check_point_tile_num = rd.choice([ind for ind, value in enumerate(sum(self.map_data)) if value == 3])


    def generate_maze(self):
        maze = np.zeros((self.height, self.width), dtype=int)
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 1
        stack = [(start_x, start_y)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            current_x, current_y = stack[-1]
            rd.shuffle(directions)
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < self.width - 1 and 0 <= ny < self.height - 1 and maze[ny][nx] == 0:
                    maze[current_y + dy // 2][current_x + dx // 2] = 1
                    maze[ny][nx] = 1
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

        maze[1][0] = 0
        maze[self.height - 2][self.width - 2] = 1
        maze[self.height - 2][self.width - 1] = 1
        maze[self.height - 2][self.width - 3] = 1
        return maze.flatten()


    def make_map_picture(self, map_num, combined_surf, road_image, checkpoint_image, wall_image):
        now_map = self.map_data[map_num]
        for i in range(self.mapsize):
            if now_map[i] == 1:
                image = road_image

            if i == self.check_point_tile_num:
                image = checkpoint_image
            elif now_map[i] == 0:
                image = wall_image

            x, y = self.coords[i]
            combined_surf.blit(image, (x, y))
        pygame.image.save(combined_surf, f'MAZE_MAP{map_num + 1}.png')


    def update_now_map_data(self, map_num):
        self.now_map_data = self.map_data[map_num]


    def controll_exit_tile(self, screen, is_player_passed_checkpoint, road_image, wall_image):
        if is_player_passed_checkpoint:
            screen.blit(road_image, self.coords[ self.exit_tile_num ])
            if self.now_map_data[ self.exit_tile_num ] == 0:
                self.now_map_data[ self.exit_tile_num ] = 1           
        else:
            self.now_map_data [ self.exit_tile_num ] = 0
            screen.blit(wall_image, self.coords[ self.exit_tile_num ])
