'''
1. 지금은 타이머가 미로를 가리는데, 화면 크기와 미로 맵 크기를 조금 조정해서 타이머가 존재할 공간을 위쪽에 만들기
2. 지금 나름의 필승법? 이 미로의 가운데로만 안들어가면 미로 난이도가 굉장히 쉬워지는데, 억지로 미로 가운데를 통과하게 만들지 말지, 통과하게 한다면 어떻게 할지
    루즈해질수도 있어서 유지하는게 더 나을지도
  2-1. 미로를 열기만 하는게 아니라 벽을 랜덤하게 생성하기도 하기 - 영구적으로 열리거나 닫히는게 아니라, 맵이 바뀌는 시간을 현재 5초보다 늘리고, 맵이 바뀌면 열렸거나 닫힌 것들을 원래대로 되돌리기

  2-2. 지금 맵이 바뀔 때 플레이어가 길에 있다가 바뀌고 벽과 겹치게 되면, 맵이 바뀌기 전까지 못움직이게 됨
       => 벽으로 바뀔 타일을 빨간색으로 바꾼다던지 해서 미리 경고하고, 만약 벽에 끼이면 태초로 되돌려보내기?

3. 게임 시작 화면, 에러 표시 등 UI 설정
    3-1. 게임 시작화면을 만들어서, 게임 설명? 같은 걸 넣고, pygame 의 입력 키 인식을 이용해서 숫자 키보드를 누르면 해당 값을 토대로 미로를 만들 되, isdigit이 False라면 에러를 발생시키기
    3-2. 게임 도중 벽으로는 이동 불가합니다 혹은 외벽으로는 이동이 불가합니다 등의 메세지들을 심볼? 등으로 알려주기
    3-3. 게임 종료 화면 만들기
4.
'''
import pygame
import random as rd
import time as t
import numpy as np

class OutsideBoundaryError(Exception):
    """외벽에서 이동하려고 할 경우 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)




class Maze:   #미로 게임 한 번의 데이터들을 저장할 객체, Tile 클래스에 있던 속성이나 메소드들 전부 여기로 이동됨,  전체 기능에는 변화 X, 변수 이름들이 조금 바뀌었을 수 있음
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mapsize = height * width
        self.map_data = [self.generate_maze() for _ in range(3)]
        self.coords = [(x, y) for y in range(0, self.height * 15 , 15) for x in range(0, self.width * 15, 15)]
        self.exit_tile_nums = [self.mapsize - self.width - i for i in range(1, 4)]  #탈출구의 위치는 오른쪽 아래 가로 세 칸으로 일정하게 생성됨

    def set_edge_tile_num(self):
        self.left_vertical_edge_num = [i for i in range(0, self.mapsize - self.width, self.width)]
        self.right_vertical_edge_num = [i for i in range(self.width - 2, self.mapsize - self.width - 1, self.width)]     #일반화된 각 모서리 타일번호들
        self.up_horizon_edge_num = [i for i in range(0, self.width - 1)]
        self.down_horizon_edge_num = [i for i in range(self.mapsize - 2 * self.width, self.mapsize -  self.width - 1)]

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

        maze[ 1 ][ 0 ] = 0
        maze[ self.height - 2 ][ self.width - 2 ] = 1
        maze[ self.height - 2 ][ self.width - 1 ] = 1
        maze[ self.height - 2 ][ self.width - 3 ] = 1

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
        self.now_map_data = self.map_data[ map_num ]




class Player:
    def __init__(self, tile_num, player_image, screen):
        self.tile_num = tile_num
        self.image = player_image
        self.screen = screen
        self.first_move = t.time()    #플레이어가 이동할 때마다 새 t.time() 으로 바뀌는 값
#플레이어가 너무 빨리 이동할 수 없도록 막는 역할
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
        
        if next_tile_num in maze.up_horizon_edge_num:   #각 모서리는 일정 방향키를 눌러야만 갈 수 있기 때문에, 불필요한 입력 키 확인문을 제거함
#ex): 위쪽 모서리는 UP key로만 갈 수 있음, 따라서 UP 키인지 확인은 불필요. next_tile_num 이 해당 모서리에 속하는지만 확인하면 됨
            message = "위쪽 외벽에서 위로 이동할 수 없습니다."
            
        if next_tile_num in maze.down_horizon_edge_num:
            message = "아래쪽 외벽에서 아래로 이동할 수 없습니다."
            
        if next_tile_num in maze.left_vertical_edge_num:
            message = "왼쪽 외벽에서 왼쪽으로 이동할 수 없습니다."
        
        if next_tile_num in maze.right_vertical_edge_num:
            message = "오른쪽 외벽에서 오른쪽으로 이동할 수 없습니다."
        if message:
            raise OutsideBoundaryError( message )


    def move_player(self, user_key):
        next_tile_num = self.cal_next_tile_num(user_key)
        self.check_boundary(next_tile_num)
        if maze.now_map_data[ next_tile_num ] == 1:   #Tile.obj를 제거하고, 맵 정보가 0, 1 로 저장된 now_map_data 에서 인덱스와 타일번호가 값이 일치하기 때문에 조건문을 이렇게 변형할 수 있음
            self.tile_num = next_tile_num
            return True
        else:
            print("벽이 있어 이동할 수 없습니다.")
            return False

    def show_player(self):
        x, y = maze.coords[self.tile_num]
        self.screen.blit(self.image, (x, y))


    def is_moving_too_fast(self):
        second_move = t.time()
        if second_move - self.first_move < 0.1:    #만약 이전 플레이어가 이동한 시간에서, 0,15초(추후 가장 적절한 값이 있다면 변형) 이상 지나지 않았다면, 너무 빠른 입력임(True)를 리턴해서 키 입력을 무시
            return True
        else:
            self.first_move = second_move         #0.15초 이상 지났다면,  self.first_move 을 새로 갱신해주고
            return False                       #입력시간이 적절함(False) 를 리턴해서 키 입력, 플레이어가 이동하도록 함
        
    
# Pygame 초기화
pygame.init()

# 이미지 로드 및 크기 조정
wall_image = pygame.image.load('stone_wall02.png')
wall_image = pygame.transform.scale(wall_image, (15, 15))
road_image = pygame.image.load('01tizeta_floor_e.png')
road_image = pygame.transform.scale(road_image, (15, 15))
player_image = pygame.image.load('Player.png')
player_image = pygame.transform.scale(player_image, (15, 15))

print('플레이할 미로 크기를 설정하세요. 전체 타일 개수는 3500개 미만을 추천합니다.')
x = int(input('미로의 가로 타일 개수 : '))
y = int(input('미로의 세로 타일 개수 : '))
maze = Maze(x, y)        #x, y 값을 가로, 세로 크기로 가지는 미로 데이터 객체를 생성
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

pygame.time.set_timer(pygame.USEREVENT, 5000)   #맵 바뀌는데 15초는 너무 느린것 같아 일단 5초로 설정
clock = pygame.time.Clock()
map_num = 0
maze.update_now_map_data(map_num)  # 초기 map_data 설정
player = Player(maze.width + 1, player_image, screen)


# 시간 측정을 위한 초기화
start_time = t.time()
font = pygame.font.Font(None, 36)  # 화면에 표시할 글꼴 설정

running = True

# 게임 루프
while running:
    elapsed_time = int(t.time() - start_time)  # 경과 시간 계산
    screen.blit(map_images[map_num], (0, 0))  # 맵을 매 프레임마다 다시 그리기
    player.show_player()  # 플레이어 그리기

    # 경과 시간 표시 (빨간색 글씨)
    time_surface = font.render(f"Time: {elapsed_time} sec", True, (255, 0, 0))
    screen.blit(time_surface, (10, 10))

    pygame.display.flip()  # 화면 업데이트

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

    # 게임 완료 조건 (가장 오른쪽, 가장 밑에 있는 길에 도달)
    if player.tile_num == maze.exit_tile_nums[0]:
        running = False
        print(f"게임 완료! 총 시간: {elapsed_time} 초")

    clock.tick(60)
pygame.quit()
