import pygame
import random as rd
import time as t
import numpy as np

class OutsideBoundaryError(Exception):
    """외벽에서 이동하려고 할 경우 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)

class Tile:
    coords = [(x*15, y*15) for y in range(0, 40) for x in range(0, 60)]
    mapsize = len(coords)
    left_vertical_edge_num = [i for i in range(0, 2400, 60)]
    right_vertical_edge_num = [i for i in range(59, 2400, 60)]
    up_horizon_edge_num = [i for i in range(0, 60)]
    down_horizon_edge_num = [i for i in range(2340, 2400)]
    obj = []

    def __init__(self, tile_type):
        self.tile_type = tile_type

    @staticmethod
    def generate_maze(width, height):
        maze = np.zeros((height, width), dtype=int)
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 1
        stack = [(start_x, start_y)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            current_x, current_y = stack[-1]
            rd.shuffle(directions)
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < width - 1 and 0 <= ny < height - 1 and maze[ny][nx] == 0:
                    maze[current_y + dy // 2][current_x + dx // 2] = 1
                    maze[ny][nx] = 1
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

        maze[1][0] = 0
        maze[height - 2][width - 2] = 1
        maze[height - 2][width - 1] = 1
        maze[height - 2][width - 3] = 1

        return list(maze.flatten())

    @classmethod
    def make_map_picture(cls, map_num, combined_surf):
        now_map = cls.map_data[map_num]
        for i in range(cls.mapsize):
            if now_map[i] == 0:
                image = wall_image
                cls.obj.append(cls('wall'))
            else:
                image = road_image
                cls.obj.append(cls('road'))

            combined_surf.blit(image, cls.coords[i])
        pygame.image.save(combined_surf, f'MAZE_MAP{map_num + 1}.png')

    @classmethod
    def update_map_objects(cls, map_num):
        """맵 변경 시 obj 리스트를 새로 갱신"""
        now_map = cls.map_data[map_num]
        cls.obj = []  # 기존 obj 초기화
        for tile_type in now_map:
            if tile_type == 0:
                cls.obj.append(cls('wall'))
            else:
                cls.obj.append(cls('road'))

class Player:
    def __init__(self, tile_num, player_image, screen):
        self.tile_num = tile_num
        self.image = player_image
        self.screen = screen

    def cal_next_tile_num(self, user_key):
        if user_key == 'UP':
            change = -60
        elif user_key == 'DOWN':
            change = 60
        elif user_key == 'LEFT':
            change = -1
        elif user_key == 'RIGHT':
            change = 1
        else:
            raise ValueError("잘못된 키 입력")
        return self.tile_num + change

    def check_boundary(self, next_tile_num, user_key):
        if user_key == 'UP' and self.tile_num in Tile.up_horizon_edge_num:
            raise OutsideBoundaryError("위쪽 외벽에서 위로 이동할 수 없습니다.")
        if user_key == 'DOWN' and self.tile_num in Tile.down_horizon_edge_num:
            raise OutsideBoundaryError("아래쪽 외벽에서 아래로 이동할 수 없습니다.")
        if user_key == 'LEFT' and self.tile_num in Tile.left_vertical_edge_num:
            raise OutsideBoundaryError("왼쪽 외벽에서 왼쪽으로 이동할 수 없습니다.")
        if user_key == 'RIGHT' and self.tile_num in Tile.right_vertical_edge_num:
            raise OutsideBoundaryError("오른쪽 외벽에서 오른쪽으로 이동할 수 없습니다.")

    def move_player(self, user_key):
        next_tile_num = self.cal_next_tile_num(user_key)
        self.check_boundary(next_tile_num, user_key)
        if Tile.obj[next_tile_num].tile_type == 'road':
            self.tile_num = next_tile_num
            return True
        else:
            print("벽이 있어 이동할 수 없습니다.")
            return False

    def show_player(self):
        x, y = Tile.coords[self.tile_num]
        self.screen.blit(self.image, (x, y))

    def random_move(self):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        rd.shuffle(directions)
        for direction in directions:
            next_tile_num = self.cal_next_tile_num(direction)
            if Tile.obj[next_tile_num].tile_type == 'road':
                self.tile_num = next_tile_num
                break

# Pygame 초기화
pygame.init()

# 이미지 로드 및 크기 조정
wall_image = pygame.image.load('stone_wall02.png')
wall_image = pygame.transform.scale(wall_image, (15, 15))
road_image = pygame.image.load('01tizeta_floor_e.png')
road_image = pygame.transform.scale(road_image, (15, 15))
player_image = pygame.image.load('Player.png')
player_image = pygame.transform.scale(player_image, (15, 15))

Tile.map_data = [Tile.generate_maze(60, 40) for _ in range(3)]
for i in range(3):
    combined_map = pygame.Surface((900, 600))
    Tile.make_map_picture(i, combined_map)

maze_map1 = pygame.image.load('MAZE_MAP1.png')
maze_map2 = pygame.image.load('MAZE_MAP2.png')
maze_map3 = pygame.image.load('MAZE_MAP3.png')
map_images = [maze_map1, maze_map2, maze_map3]

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Maze_Game")

pygame.time.set_timer(pygame.USEREVENT, 15000)
clock = pygame.time.Clock()
map_index = 0
Tile.update_map_objects(map_index)  # 초기 obj 설정
player = Player(61, player_image, screen)

running = True

# 게임 루프
while running:
    screen.blit(map_images[map_index], (0, 0))  # 맵을 매 프레임마다 다시 그리기
    player.show_player()  # 플레이어 그리기
    pygame.display.flip()  # 화면 업데이트

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key = "UP"
            elif event.key == pygame.K_DOWN:
                key = "DOWN"
            elif event.key == pygame.K_LEFT:
                key = "LEFT"
            elif event.key == pygame.K_RIGHT:
                key = "RIGHT"
            else:
                continue

            try:
                player.move_player(key)
            except OutsideBoundaryError as e:
                print(f"오류 발생: {e}")

        if event.type == pygame.USEREVENT:
            map_index = (map_index + 1) % len(map_images)
            Tile.update_map_objects(map_index)  # 새 맵 데이터 반영
            if Tile.obj[player.tile_num].tile_type == 'wall':
                player.random_move()  # 플레이어가 벽에 있으면 랜덤 이동

    clock.tick(60)

pygame.quit()
