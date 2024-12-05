import pygame
import random as rd
import time as t
import numpy as np


class OutsideBoundaryError(Exception):
    """외벽에서 이동하려고 할 경우 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)
        
class WidthSizeError(Exception):
    """미로 가로 크기가 지정 범위 (20 ~ 70) 을 벗어날 때 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)

class HeightSizeError(Exception):
    """미로 세로 크기가 지ㅓ범위 (10 ~ 60) 을 벗어날 때 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)

class InvalidValueError(Exception):
    """입력받은 미로 크기가 정수형이 아닐 때 발생하는 사용자 정이 예외"""
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





class ScreenManager:

    @staticmethod
    def blit_image_center(screen, image, y):
        screen.blit(image, (screen.get_width() // 2 - image.get_width() // 2, int(y)))

    @staticmethod
    def show_starting_screen(screen):
        screen.fill((102, 153, 204))
        font_ = pygame.font.Font(None, 36)
        enter_to_start = font_.render('Press Enter To START !', True, (102, 255, 255))
        screen.blit( enter_to_start,
                     (screen.get_width() // 2 - enter_to_start.get_width() // 2, 600))
        pygame.display.flip()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print('Enter_key is pushed.')
                        running = False
                        break
                        
    @staticmethod
    def perceive_input_key():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                        return '1'
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                        return '2'
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                        return '3'
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                        return '4'
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                        return '5'
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                        return '6'
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                        return '7'
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                        return '8'
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                        return '9'
                    elif event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                        return '0'
                    else:
                        continue

    @classmethod
    def input_maze_size(cls, screen, font):
            message_type = ['horizontal', 'vertical']
            width_height = []
            for i in range(2):
                size = ['_']*2
                input_message = font.render(f"""Type {message_type[i]} tile amount of maze you'll play!""", True, (102, 255, 255))
                warning_message = pygame.font.Font(None, 23).render("the size must be two-digit", True, (102, 255, 255))
                screen.fill((102, 153, 204))
                cls.blit_image_center(screen, input_message, 560)
                cls.blit_image_center(screen, warning_message, 580)
                pygame.display.flip()
                
                for j in range(2):
                    user_input = cls.perceive_input_key()
                    size[j] = user_input
                    font_ = pygame.font.Font(None, 20)
                    typed_value = font_.render(f"{''.join(size)}", True, (102, 255, 255))
                    cls.blit_image_center(screen, typed_value, 620)
                    pygame.display.flip()
                width_height.append(int(''.join(size)))
            return width_height
                    
    def show_set_mapsize_screen(self, screen):
        screen.fill((102, 153, 204))
        font_ = pygame.font.Font(None, 36)
        return map(int, self.input_maze_size(screen, font_))

        

    @staticmethod
    def show_ending_screen(screen, elapsed_time):
        ending_font = pygame.font.Font(None, 72)
        message_font = pygame.font.Font(None, 36)

        screen.fill((0, 0, 0))  # 배경을 검은색으로 설정
        ending_message = ending_font.render("GAME CLEAR!", True, (255, 255, 0))
        time_message = message_font.render(f"total time: {elapsed_time} sec", True, (255, 255, 255))
        restart_message = message_font.render("Press 'm' to play again", True, (255, 255, 255))

        screen.blit(ending_message, (screen.get_width() // 2 - ending_message.get_width() // 2, 
                                      screen.get_height() // 2 - ending_message.get_height() // 2 - 20))
        screen.blit(time_message, (screen.get_width() // 2 - time_message.get_width() // 2, 
                                    screen.get_height() // 2 + time_message.get_height() // 2))
        screen.blit(restart_message, (screen.get_width() // 2 - restart_message.get_width() // 2, 
                                       screen.get_height() // 2 + time_message.get_height() + 20))

        pygame.mixer.Sound('sound_clear.mp3').play(-1)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        waiting_for_input = False  # 게임을 다시 시작하기 위한 플래그
        pygame.quit()  # 이전 게임 종료


def restart_game():
    # Pygame 초기화
    pygame.init()
    pygame.mixer.init()

    # 배경음악과 효과음 설정
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(-1)  # 반복 재생
    pygame.mixer.music.set_volume(0.5)

    # 이미지 로드 및 크기 조정
    global wall_image, road_image, player_image, maze
    wall_image = pygame.image.load('stone_wall02.png')
    wall_image = pygame.transform.scale(wall_image, (15, 15))
    road_image = pygame.image.load('01tizeta_floor_e.png')
    road_image = pygame.transform.scale(road_image, (15, 15))
    player_image = pygame.image.load('Player.png')
    player_image = pygame.transform.scale(player_image, (15, 15))

    # 게임 설정
    screen = pygame.display.set_mode((900, 700))
    screen_manager = ScreenManager()
    screen_manager.show_starting_screen(screen)
    x, y = screen_manager.show_set_mapsize_screen(screen)

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
            Screen.show_ending_screen(screen, elapsed_time)
            running = False

        clock.tick(60)

# 메인 게임 루프
while True:
    restart_game()
