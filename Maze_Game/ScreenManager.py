import pygame
import time as t
import sys
from Exceptions import *

class ScreenManager:
    @staticmethod
    def show_gamerule_intro_screen(screen, image_list):
        font_ = pygame.font.Font(None, 28)
        enter_message = font_.render('Press Enter to go to next.', True, (152, 255, 240))
        image_list = list(map(lambda image: pygame.transform.scale(image, (100, 100)), image_list))
        messages = ['''The Road Tile. You can move on Road Tile by four keys.\W-UP, A-LEFT, S-DOWN, D-RIGHT.\And MINIMUM INTERVAL of each move is 0.14s.\You can't move faster than that''',
                    '''The Wall Tile. You can't move torwards that.\And if you stuck in wall when map has just changed,\you will TP to start_point''',
                    '''This is you.\Keep your eyes on it !''',
                    '''The checkpoint.\You must pass this tile At Least Once''']
        screen.fill((102, 153, 204))
        for i in range(4):
            screen.fill((102, 153, 204))
            message_lines = messages[i].split("\\")
            y_offset = 250
            
            for line in message_lines:
                message = font_.render(line, True, (120, 240, 240))
                screen.blit(message, (30, y_offset))
                y_offset += 40

            screen.blit(image_list[i], (700, 350))
            screen.blit(enter_message, (30, 400))
            pygame.display.flip()
            
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            running = False
                            break
            

    @staticmethod
    def blit_image_center(screen, image, y):
        screen.blit(image, (screen.get_width() // 2 - image.get_width() // 2, int(y)))

    @classmethod
    def show_starting_screen(cls, screen, image_list):
        screen.fill((102, 153, 204))
        enter_to_start = pygame.font.Font(None, 36).render('Press Enter To START !', True, (102, 255, 255))
        E_to_explanation = pygame.font.Font(None, 36).render('Press A for some explanation !', True, (152, 255, 240))
        game_title = pygame.font.Font(None, 100).render('Maze Escape', True, (100, 240, 255))
        cls.blit_image_center(screen, game_title, 180)
        cls.blit_image_center(screen, enter_to_start, 600)
        cls.blit_image_center(screen, E_to_explanation, 550)
        pygame.display.flip()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        cls.show_gamerule_intro_screen(screen, image_list)
                        
                    if event.key == pygame.K_RETURN:
                        running = False
                        break
                        
    @staticmethod
    def perceive_input_key():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
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
    def input_maze_size(cls, screen):
            message_type = ['Width', 'Height']
            width_height = []
            for i in range(2):
                while True:
                    size = ['_']*2
                    screen.fill((102, 153, 204))
                    input_message = pygame.font.Font(None, 36).render(f"""Type {message_type[i]} ( tile amount ) of maze you'll play   using num_key !""", True, (102, 255, 255))
                    warning_message = pygame.font.Font(None, 27).render("the size must be two-digit !", True, (90, 255, 255))
                    input_blank = pygame.font.Font(None, 40).render(f"{' '.join(size)} Tiles", True, (102, 255, 255))
                    announce_of_type = pygame.font.Font(None, 36).render(f'{message_type[i]}', True, (102, 255, 255))
                    cls.blit_image_center(screen, input_message, 560)
                    cls.blit_image_center(screen, warning_message, 600)
                    cls.blit_image_center(screen, input_blank, 300)
                    cls.blit_image_center(screen, announce_of_type, 270)
                    pygame.display.flip()
                    
                    for j in range(2):
                        user_input = cls.perceive_input_key()
                        size[j] = user_input
                        input_blank = pygame.font.Font(None, 40).render(f"{' '.join(size)} Tiles", True, (102, 255, 255))
                        cls.blit_image_center(screen, input_blank, 300)
                        pygame.display.flip()
                        if j == 1:
                            t.sleep(0.5)
                    try:
                        check_value = int(''.join(size))
                        if i == 0 and check_value not in range(20, 71):
                            raise WidthSizeError('width must be in (20 ~ 70)')
                        elif i == 1 and check_value not in range(10, 51):
                            raise HeightSizeError('height must be in (10 ~ 50)')

                    except WidthSizeError as e:
                        error_message = e.args[0]
                    except HeightSizeError as e:
                        error_message = e.args[0]
                    else:
                        error_message = ''
                        width_height.append( check_value )
                        break
                        
                    finally:
                        if error_message:
                            error_message = pygame.font.Font(None, 40).render(error_message, True, (204, 0, 0))
                            cls.blit_image_center(screen, error_message, 500)
                            pygame.display.flip()
                            t.sleep(1.6)
                            
            return width_height

                    
    def show_set_mapsize_screen(self, screen):
        screen.fill((102, 153, 204))
        return map(int, self.input_maze_size(screen))
    

    @classmethod
    def show_ending_screen(cls, screen, elapsed_time):
        ending_font = pygame.font.Font(None, 50)
        message_font = pygame.font.Font(None, 25)

        screen.fill((0, 0, 0))
        ending_message = ending_font.render("GAME CLEAR!", True, (255, 255, 0))
        time_message = message_font.render(f"total time: {elapsed_time} sec", True, (255, 255, 255))
        restart_message = message_font.render("Press 'm' to play again", True, (255, 255, 255))
        close_message = pygame.font.Font(None, 25).render("Press 'esc' to end game", True, (255, 255, 255))

        cls.blit_image_center(screen, ending_message, screen.get_height() // 2 - ending_message.get_height() // 2 - 20)
        cls.blit_image_center(screen, time_message, screen.get_height() // 2 + time_message.get_height() // 2)
        cls.blit_image_center(screen, restart_message, screen.get_height() // 2 + time_message.get_height() + 20)
        cls.blit_image_center(screen, close_message, screen.get_height() // 2 + close_message.get_height() + 33)

        pygame.mixer.music.stop()
        pygame.mixer.Sound('Data_Sets/clear_sound.mp3').play()
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        waiting_for_input = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
