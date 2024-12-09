from Maze_Game_pkg.ScreenManager import ScreenManager
from Maze_Game_pkg.Player import Player
from Maze_Game_pkg.Maze import Maze
from Maze_Game_pkg.Exceptions import *
import pygame
import time as t
import sys

def main():
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load('Maze_Game_pkg/Data_Sets/bgm.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    global wall_image, road_image, player_image, checkpoint_image, maze
    wall_image          = pygame.image.load('Maze_Game_pkg/Data_Sets/wall_tile.png')
    road_image         = pygame.image.load('Maze_Game_pkg/Data_Sets/road_tile.png')
    player_image       = pygame.image.load('Maze_Game_pkg/Data_Sets/Player.png')
    checkpoint_image = pygame.image.load('Maze_Game_pkg/Data_Sets/checkpoint.png')

    before_game_screen = pygame.display.set_mode((900, 700))
    screen_manager = ScreenManager()
    screen_manager.show_starting_screen(before_game_screen, [road_image, wall_image, player_image, checkpoint_image])
    x, y = screen_manager.show_set_mapsize_screen(before_game_screen) 
    
    wall_image          = pygame.transform.scale(wall_image, (15, 15))
    road_image         = pygame.transform.scale(road_image, (15, 15))
    player_image       = pygame.transform.scale(player_image, (15, 15))
    checkpoint_image = pygame.transform.scale(checkpoint_image, (15, 15))


    maze = Maze(x, y)
    for i in range(3):
        combined_map = pygame.Surface((15 * maze.width, 15 * maze.height + 45))
        maze.make_map_picture(i, combined_map, road_image, checkpoint_image, wall_image)

    maze_map1 = pygame.image.load('MAZE_MAP1.png')
    maze_map2 = pygame.image.load('MAZE_MAP2.png')
    maze_map3 = pygame.image.load('MAZE_MAP3.png')
    map_images = [maze_map1, maze_map2, maze_map3]

    game_screen = pygame.display.set_mode((15 * maze.width, 15 * maze.height + 45))
    pygame.display.set_caption("Maze_Game")

    pygame.time.set_timer(pygame.USEREVENT, 5000)
    clock = pygame.time.Clock()
    map_num = 0
    maze.update_now_map_data(map_num)
    player = Player(maze.width + 1, player_image, game_screen)

    start_time = t.time()
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        elapsed_time = int(t.time() - start_time)
        game_screen.blit(map_images[map_num], (0, 0))
        maze.controll_exit_tile(game_screen, player.passed_checkpoint, road_image, wall_image)
        player.show_player(maze)

        time_surface = font.render(f"Time: {elapsed_time} sec", True, (255, 0, 0))
        game_screen.blit(time_surface, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if player.is_moving_too_fast():
                    continue
                if event.key == pygame.K_w:
                    key = "UP"
                elif event.key == pygame.K_s:
                    key = "DOWN"
                elif event.key == pygame.K_a:
                    key = "LEFT"
                elif event.key == pygame.K_d:
                    key = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    continue

                try:
                    player.move_player(key, maze)
                except MoveToWallError:
                    pygame.mixer.Sound('Maze_Game_pkg/Data_Sets/hit_wall_sound.wav').play()
                except CheckpointNotPassedError as e:
                    unchecked_message = pygame.font.Font(None, 18).render(e.args[0], True, (255, 0, 0))
                    game_screen.blit(unchecked_message, (time_surface.get_width() + 20, 20))
                    pygame.mixer.Sound('Maze_Game_pkg/Data_Sets/hit_wall_sound.wav').play()
                    pygame.display.flip()
                    t.sleep(0.1)

            if event.type == pygame.USEREVENT:
                map_num = (map_num + 1) % len(map_images)
                maze.update_now_map_data(map_num)
                player.is_stuck_in_wall(maze)

        if player.tile_num == maze.exit_tile_num:
                ScreenManager.show_ending_screen(game_screen, elapsed_time)
                main()

        clock.tick(60)

if __name__ == "__main__":
    main()
