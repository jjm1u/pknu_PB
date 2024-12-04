import pygame
import random as rd
import time as t
import numpy as np


class OutsideBoundaryError(Exception):
    """외벽에서 이동하려고 할 경우 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mapsize = height * width
        self.map_data = [self.generate_maze() for _ in range(3)]
        self.coords = [(x, y) for y in range(0, self.height * 15, 15) for x in range(0, self.width * 15, 15)]
        self.exit_tile_nums = [self.mapsize - self.width - i for i in range(1, 4)]

    def set_edge_tile_num(self):
        self.left_vertical_edge_num = [i for i in range(0, self.mapsize - self.width, self.width)]
        self.right_vertical_edge_num = [i for i in range(self.width - 2, self.mapsize - self.width - 1, self.width)]
        self.up_horizon_edge_num = [i for i in range(0, self.width - 1)]
        self.down_horizon_edge_num = [i for i in range(self.mapsize - 2 * self.width, self.mapsize - self.width - 1)]

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

        return list(maze.flatten())

    def make_map_picture(self, map_num, combined_surf):
        now_map = self.map_data[map_num]
        for i in range(self.mapsize):
            if now_map[i] == 0:
                image = wall_image
            else:
                image = road_image

            combined_surf.blit(image, self.coords[i])
        pygame.image.save(combined_surf, f'MAZE_MAP{map_num + 1}.png')

    def update_now_map_data(self, map_num):
        self.now_map_data = self.map_data[map_num]


class Player:
    def __init__(self, tile_num, player_image, screen):
        self.tile_num = tile_num
        self.image = player_image
        self.screen = screen
        self.first_move = t.time()

    def cal_next_tile_num(self, user_key):
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

    @staticmethod
    def check_boundary(next_tile_num):
        message = ""
        if next_tile_num in maze.exit_tile_nums:
            return

        if next_tile_num in maze.up_horizon_edge_num:
            message = "위쪽 외벽에서 위로 이동할 수 없습니다."
        if next_tile_num in maze.down_horizon_edge_num:
            message = "아래쪽 외벽에서 아래로 이동할 수 없습니다."
        if next_tile_num in maze.left_vertical_edge_num:
            message = "왼쪽 외벽에서 왼쪽으로 이동할 수 없습니다."
        if next_tile_num in maze.right_vertical_edge_num:
            message = "오른쪽 외벽에서 오른쪽으로 이동할 수 없습니다."
        if message:
            raise OutsideBoundaryError(message)

    def move_player(self, user_key):
        next_tile_num = self.cal_next_tile_num(user_key)
        self.check_boundary(next_tile_num)
        if maze.now_map_data[next_tile_num] == 1:
            self.tile_num = next_tile_num
            pygame.mixer.Sound('sound.mp3').play()
            return True
        else:
            print("벽이 있어 이동할 수 없습니다.")
            pygame.mixer.Sound('sound_wall.mp3').play()
            return False

    def show_player(self):
        x, y = maze.coords[self.tile_num]
        self.screen.blit(self.image, (x, y))

    def is_moving_too_fast(self):
        second_move = t.time()
        if second_move - self.first_move < 0.1:
            return True
        else:
            self.first_move = second_move
            return False


# Pygame 초기화
pygame.init()
pygame.mixer.init()

# 배경음악과 효과음 설정
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)  # 반복 재생
pygame.mixer.music.set_volume(0.5)

# 이미지 로드 및 크기 조정
wall_image = pygame.image.load('stone_wall02.png')
wall_image = pygame.transform.scale(wall_image, (15, 15))
road_image = pygame.image.load('01tizeta_floor_e.png')
road_image = pygame.transform.scale(road_image, (15, 15))
player_image = pygame.image.load('Player.png')
player_image = pygame.transform.scale(player_image, (15, 15))

# 게임 설정
print('플레이할 미로 크기를 설정하세요. 전체 타일 개수는 3500개 미만을 추천합니다.')
x = int(input('미로의 가로 타일 개수 : '))
y = int(input('미로의 세로 타일 개수 : '))
maze = Maze(x, y)
maze.set_edge_tile_num()
for i in range(3):
    combined_map = pygame.Surface((15 * maze.width, 15 * maze.height))
    maze.make_map_picture(i, combined_map)

maze_map1 = pygame.image.load('MAZE_MAP1.png')
maze_map2 = pygame.image.load('MAZE_MAP2.png')
maze_map3 = pygame.image.load('MAZE_MAP3.png')
map_images = [maze_map1, maze_map2, maze_map3]

screen = pygame.display.set_mode((15 * maze.width, 15 * maze.height))
pygame.display.set_caption("Maze_Game")

pygame.time.set_timer(pygame.USEREVENT, 5000)
clock = pygame.time.Clock()
map_num = 0
maze.update_now_map_data(map_num)
player = Player(maze.width + 1, player_image, screen)

start_time = t.time()
font = pygame.font.Font(None, 36)

running = True

# 게임 루프
while running:
    elapsed_time = int(t.time() - start_time)
    screen.blit(map_images[map_num], (0, 0))
    player.show_player()

    time_surface = font.render(f"Time: {elapsed_time} sec", True, (255, 0, 0))
    screen.blit(time_surface, (10, 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if player.is_moving_too_fast():
                continue
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
            map_num = (map_num + 1) % len(map_images)
            maze.update_now_map_data(map_num)

    if player.tile_num == maze.exit_tile_nums[0]:
        running = False
        print(f"게임 완료! 총 시간: {elapsed_time} 초")

    clock.tick(60)
pygame.quit()
