'''랜덤한 맵을 만드는 것까지 가능한 코드지만 해당 알고리즘을 아직 이해 못함
작동은 아주 잘됨
그 외에 창 크기를 보기 편하게 조금 조절한 것 말고는 기존 코드랑 똑같음'''
import pygame
import random as rd
import time as t
import numpy as np

'''
pygame으로 만든 창은 좌표가 왼쪽 위에서부터 시작함 (0, 0)
오른쪽과 아래쪽으로 갈수록 x, y 좌표가 각각 증가함
'''
class Tile:
    coords = [(x*15, y*15) for y in range(0, 40) for x in range(0, 60)]    # coordinates(좌표) 의 약자
    #각 타일을 위치시킬 좌표. 게임 화면이 미로로 꽉 차도록 (0, 0) (왼쪽 위부터 시작하고, 현재 플레이어, 타일 등 모든 이미지의 크기는
    #15 * 15 크기로 해놨기 때문에 이웃한 좌표간에 x, y 각각 15씩 차이가 남
    #원래 타일번호는 왼쪽 위부터 1에서 시작하도록 하려고 했는데, 생각해보니 리스트 요소들이 가지는 인덱스를 타일번호로써 대체해도 되겠다 싶어서 타일번호는 0부터 시작하는 개념으로 바꿈
    #따라서 coords에 위치한 좌표들의 인덱스가 바로 해당 좌표의 타일번호임
    mapsize = len(coords)
    left_vertical_edge_num    = [i for i in range(0, 2400, 60)]     #왼쪽 모서리 타일번호, Left 키를 눌렀을 때, 플레이어의 unique_num이 여기 속한다면 이동하지 않음
    right_vertical_edge_num  = [i for i in range(0, 60)]            #오른쪽 모서리 타일번호  Right 키
    up_horizon_edge_num     = [i for i in range(59, 2400, 60)]    #위쪽 모서리 타일번호    Up 키
    down_horizon_edge_num = [i for i in range(2399, 2400)]        #아래쪽 모서리 타일번호    Down 키
#왼쪽 세로축 모서리 0, 60, 120, 180, 240.....2279, 2339
#위쪽 가로축 모서리 0, 1, 2, 3....58, 59
#오른쪽 세로축 모서리 58, 118, 178, 238....2338, 2398
#아래쪽 가로축 모서리 2279, 2280, ..2341....2339
    obj = []  #길과 벽이 구분없이 타일번호 순서대로 저장될 리스트 (object)
    def __init__(self, tile_type):
        self.tile_type = tile_type   #각 tile 객체들은 길인지 벽인지 인스턴스 속성으로 지니고 있음


    @classmethod
    def is_road(cls, tile_num):
        return unique_num in cls.road    #특정 unique_num의 타일이 길이면 True, 벽이면 False

#원래 계획한 미로 맵을 만드는 방식은 맵이 바뀔 때마다 미로 맵 정보가 바뀌고, 그에 따라 길, 벽 이미지들을 각 고유번호에 따른 좌표에 위치시키는 거였는데,
#해당 방식으로 구현하니까 렉이 어마어마하게 걸려서
#우선 세 개의 미로 맵 각각의 정보에 따라 맵을 만들기는 하되, 해당 이미지를 다시 다운받아서 각 맵들을 이미지로 저장하고, 맵이 바뀔 때마다 1000개가 넘는 이미지들을 매 번
#배치하는게 아니라 맵의 이미지만 들고 오도록 만듬
    @staticmethod
    def generate_maze(width, height):
        '''이 함수가 GPT한테 물어봐서 만든 랜덤 미로 맵 만드는 알고리즘인데, 활용하면 아주 좋지 아직 이해를 못해서 난감
        랜덤한 미로를 만드는 함수라고만 생각하고 넘어가도 됨
        return 값은 0과 1로 이루어진 리스트'''
        # 미로를 벽(0)로 초기화
        maze = np.zeros((height, width), dtype=int)
        # 시작 지점 (무조건 홀수로 설정)
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 1  # 시작점을 길(1)로 설정
        # 스택을 이용한 DFS 구현
        stack = [(start_x, start_y)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # 상, 하, 좌, 우로 2칸씩 이동
        while stack:
            current_x, current_y = stack[-1]
            rd.shuffle(directions)  # 랜덤하게 방향 선택
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < width - 1 and 0 <= ny < height - 1 and maze[ny][nx] == 0:
                    # 중간 벽 제거
                    maze[current_y + dy // 2][current_x + dx // 2] = 1
                    # 다음 칸을 길로 설정
                    maze[ny][nx] = 1
                    stack.append((nx, ny))
                    break
            else:
                # 더 이상 갈 곳이 없으면 스택에서 제거 (백트래킹)
                stack.pop()
        # 입구와 출구 설정
        maze[1][0] = 0  # 왼쪽 위 입구
        maze[height - 2][width - 2] = 1  # 오른쪽 아래 출구로 나갈 수 있는 길 추가
        maze[height - 2][width - 1] = 1  # 오른쪽 아래 출구
        maze[height - 2][width - 3] = 1  # 오른쪽 아래 출구로 나갈 수 있는 길 추가  (오른쪽 아래의 ㅡ자 모양 3개가 이 코드 세 줄로 만들어짐)

        # 1차원 리스트로 변환
        maze_flat = list(maze.flatten())

        return maze_flat



    @classmethod
    def make_map_picture(cls, map_num, combined_surf):   #combined_surf는 길, 벽들을 배치시켜 만들 하나의 미로 맵 이미지,          map_num은 세 개의 맵 중에 어떤 맵으로 바뀔지 알려줌
        now_map = cls.map_data[map_num]                     #Tile 클래스 속성인 맵 세개의 데이터 (0, 1)리스트에서 map_num(0, 1, 2의 값) 에 해당하는 맵 데이터를 now_map으로 저장
        for i in range(cls.mapsize):                                   # mapsize 는 len(now_map) 과 값이 같음 즉,  i는 now_map의 인덱스를 의미  (i ~ 0, 2023)
#한마디로 i 가     2400개의 0, 1이 들어있는 리스트의 인덱스이자, 각 tile들의 타일번호
            if now_map[i] == 0:                      #now_map의 i번째 값이 0이면 벽 이미지와 객체를
                image = wall_image
                cls.obj.append( cls('wall') )
            else:
                image = road_image
                cls.obj.append( cls('road') )          #1이면 길 이미지와 객체를

            combined_surf.blit(image, cls.coords[i])             #
        pygame.image.save(combined_surf, f'MAZE_MAP{map_num+1}.png') #이 스크립트 파일이 있는 위치에 MAZE_MAP 이라는 이미지를 다운로드 시키는데, 각 맵마다 1, 2, 3으로 구분이 되도록 MAZE_MAP 뒤에
        #format으로 map_num + 1 을 해줌





class Player:
    def __init__(self, tile_num, player_image, screen):  #(순서대로 타일번호, 플레이어의 이미지, 전체 게임 화면(900px X 600px))
        self.tile_num = tile_num
        Player.image = player_image                       #플레이어의 이미지를 Player 클래스 속성ㅇ에 추가
        Player.show_player(tile_num, screen)         # 이 클래스의 맨 밑에 정의되있는 함수인데, 타일번호를 받아서 해당 타일로 플레이어를 이동시키는 함수임

    def cal_next_tile_num(self, user_key):  #user_key는 유저가 누른 방향키의 종류(ex, up, down, left, right)
        if user_key == 'UP':
            change = -60                       #맵이 60 * 40 크기일 때, 한 칸 위로 가면 숫자가 60 작아짐
        elif user_key == 'DOWN':                    # down 이면 60이 커짐
            change = 60
        elif user_key == 'RIGHT':
            change = 1                         #오른쪽으로 가면 1 커짐
        elif user_key == 'LEFT':
            change = -1                        #왼쪽으로 가면 1 작아짐
        next_tile_num = self.tile_num + change    #플레이어가 이동될 고유번호를    기존의 고유번호에 변화량을 더해줘서 계산
        return next_tile_num

    def get_now_tile_num(self):
      return self.tile_num

    @classmethod
    def show_player(cls, tile_num, screen): #이동시킬 타일번호와, 전체 게임 화면을 받음
        x, y = Tile.coords[ tile_num ]         #Tile클래스에 있는 좌표(x, y 의 튜플) 리스트 coords에서 이동시킬 타일번호의 좌표를 가져옴
        screen.blit(cls.image, (x, y))      #screen.blit 은 screen이라는 화면에 원하는 이미지를, 원하는 좌표에 그리는 함수 즉, 여기선 플레이어 이미지를 좌표 (x, y) 에 그림

#여기까지가 클래스&함수





pygame.init()

wall_image   = pygame.image.load('stone_wall02.png')                  #미리 다운로드된 벽 이미지를 wall_image 에 저장
wall_image   = pygame.transform.scale(wall_image, (15, 15))           # 그대로 불러오면 크기가 굉장히 크기 때문에 게임 화면에 적절하도록 크기를 15px * 15px로 줄여서 가져옴
road_image   = pygame.image.load('01tizeta_floor_e.png')              #길 이미지 저장
road_image   = pygame.transform.scale(road_image, (15, 15))           #크기 15px X 15px 로 수정
player_image = pygame.image.load('Player.png')                        #플레이어 이미지 저장
player_image = pygame.transform.scale(player_image, (15, 15))         #크기 15px X 15px 로 수정

Tile.map_data = [Tile.generate_maze(60, 40) for _ in range(3)]       #Tile 클래스에 있는 generate_maze 함수로 랜덤한 미로 맵 0, 1 리스트를 3번 만들어서, [[맵 데이터], [맵 데이터], [맵 데이터]] 형태의
#리스트를 map_data 라는 이름으로 Tile 클래스에 저장
for i in range(3):
    combined_map = pygame.Surface((900, 600))                   #2400개의 타일들을 배치시켜서 하나의 미로 맵 이미지가 될 바탕(surface) 을 60 * 15px X 40 * 15px 의 크기로 만들어서 미로 맵과 크기가 같도록 설정
    Tile.make_map_picture(i, combined_map)                        # 맵 데이터를 받아서 하나의 맵 이미지를 만들고 다운로드 하는 make_map_picture 함수를 실행


maze_map1 = pygame.image.load('MAZE_MAP1.png')
maze_map2 = pygame.image.load('MAZE_MAP2.png')              #바로 위에서 저장된 맵 이미지 세 개를 다운로드
maze_map3 = pygame.image.load('MAZE_MAP3.png')
map_images = [maze_map1, maze_map2, maze_map3]

screen = pygame.display.set_mode((900, 600))  # 전체 게임 화면 크기를 미로 전체에 맞게 설정
pygame.display.set_caption("Maze_Game")      #게임 창 위에 나타날 제목 설정

pygame.time.set_timer(pygame.USEREVENT, 15000)  #15초마다   USEREVENT 라는 이벤트를 발생시킴 일정한 주기마다 맵을 바꾸기 위한 용도
clock = pygame.time.Clock()              #원활한 프로그램 작동을 위해 (이거 없으면 맵 바뀔때나 창을 끌 때 랙이 많이 걸림)게임의 실행속도 (fps) 를 일정하게 제한하기 위한 용도
screen.blit( map_images[0], (0, 0) ) #현재 USEREVENT가 15초마다 작동(pygame.time.set_timer(pygame.USEREVENT, 15000))가 실행되고 15초 이후) 하기 때문에 맨 처음에는 미로 맵이 띄워지지 않은 상태
#따라서 게임이 시작하기 전 미리 0번째 맵을 업로드
map_index = 1 #다음번에 1번맵을 띄우도록 +1
player = Player(61, player_image, screen)
running = True

#게임 루프 부분
while running:
    for event in pygame.event.get():   #pygame 에 있는 모든 이벤트들(사용자 지정 이벤트까지)을 전부 들고 옴
        if event.type == pygame.QUIT:   #게임 창을 alt f4 가 아닌 마우스로 끌 때 발생하는 이벤트이며 해당 이벤트 발생 시 running을 False로 설정해서 게임을 종료시킴
            running = False

        elif event.type == pygame.KEYDOWN:     #화살표 방향 키를 눌렀을 때 작동
            if event.key == pygame.K_UP:
                key = "UP"
            elif event.key == pygame.K_DOWN:       #네 개의 방향키 중 어떤 방향키인지 key에 할당
                key = "DOWN"
            elif event.key == pygame.K_LEFT:
                key = "LEFT"
            elif event.key == pygame.K_RIGHT:
                key = "RIGHT"
            else : continue
            next_unique_num = player.cal_next_unique_num(key)  #플레이어의 다음 unique_num을 계산하는 함수에 인식된 키를 넣어서 next_unique_num에 할당



        if event.type == pygame.USEREVENT:  #15초가 지나서 USEREVENT 라는 event가 발생하면 해당 if문 작동
            if map_index == len(map_images):          #맵이 3개(mpas의 인덱스가 최대 2)기 때문에, 다른 미로맵을 띄우기 전에, 만약 map_index가 2였다면(이전 맵이 2였다면), 0으로 초기화
                map_index = 0
            screen.blit(map_images[map_index], (0, 0))  #다음 미로 맵 사진 업로드
            map_index += 1    #다음번 실행때는 다음 맵이 업로드 되도록 +1
            player.show_player(61, screen)

    pygame.display.flip()
    clock.tick(60)  #게임 실행속도 제한

pygame.quit()