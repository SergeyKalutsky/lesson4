import pygame
import game_object
import game_menu
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.background_img = pygame.image.load("background.png").convert()
        pygame.display.set_caption("Platformer")
        self.all_sprite_list = pygame.sprite.Group()
        self.player = game_object.Player(20, 540)
        self.all_sprite_list.add(self.player)
        self.platform_list = pygame.sprite.Group()
        self.create_walls()
        self.artifact_list = pygame.sprite.Group()
        self.create_artifacts()
        self.player.platforms = self.platform_list
        self.player.artifacts = self.artifact_list
        self.clock = pygame.time.Clock()
        self.state = "GAME"
        self.main_menu = game_menu.MainMenu(300, 200)
        self.top_panel = game_menu.TopPanel()
        
    def create_artifacts(self):
        # Создаем артефакты (монеты) в игре
        artifact_coords = [
            [170, 405],
            [320, 410],
            [370, 510],
            [420, 310],
            [565, 505],
            [745, 485]
        ]
        for coord in artifact_coords:
            artifact = game_object.Artifact(coord[0], coord[1])
            self.artifact_list.add(artifact)
            self.all_sprite_list.add(artifact)

    def create_walls(self):
        # Создаем стены и платформы
        platform_coords = [
            [0, 0, 10, 600],
            [790, 0, 10, 600],
            [0, 590, 600, 10],
            [450, 500, 20, 100],
            [250, 550, 20, 60],
            [550, 450, 250, 10]
        ]
        for coord in platform_coords:
            platform = game_object.Platform(coord[0], coord[1], coord[2], coord[3])
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)
        

    def handle_state(self, event):
        if self.state == 'GAME':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()
                elif event.key == pygame.K_SPACE:
                    self.state = 'PAUSE'

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
                

        # Если игра не идет, значит на экране главное меню
        # Обрабатываем события главного меню:
        else:
            # Получаем кнопку, на которую нажали в главном меню:
            active_button = self.main_menu.handle_mouse_event(event.type)
            if active_button:
                # После того, как на кнопку нажали, возвращаем ее состояние в "normal":
                active_button.state =  'normal'

                # Нажали на кнопку START, перенесем персонажа в начальное  и начнем игру:
                if active_button.name == 'START':
                    self.player.rect.x = 10
                    self.player.rect.y = 10
                    self.player.change_x = 0
                    self.player.change_y = 0
                    self.state = 'GAME'

                # На паузе и нажали CONTINUE, переведем игру с состояние GAME:
                elif active_button.name == 'CONTINUE':
                    self.state = 'GAME'

                # Нажали на QUIT - завешим работу приложения:
                elif active_button.name == 'QUIT':
                    pygame.quit()
    while True:
        for a in range(0,60):
            f2 = pygame.font.SysFont('serif', 48)
            text1 = f2.render("Ты проиграл", False,(0, 180, 0))
            text2 = f2.render(a, False,(0, 180, 0))
            sc.blit(text2, (10, 50))
        if a<=0:
            sc.blit(text1, (10, 50))

    def draw_states(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_img, [0, 0])
        self.top_panel.draw(self.screen)

        if self.state == 'START':
            self.main_menu.draw(self.screen)

        elif self.state == 'GAME':
            self.all_sprite_list.draw(self.screen)

        elif self.state == 'PAUSE':
            # print('PAUSE')
            self.platform_list.draw(self.screen)
            self.main_menu.draw(self.screen)

        elif self.state == 'FINISH':
            self.main_menu.draw(self.screen)
    

    def run(self):
        done = False
        # Запустили главный игровой цикл:
        while not done:
            # print(self.state)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # Обрабатываем события для разных состояний:
                self.handle_state(event)

            # Если идет игра, обновляем все объекты в игре:
            if self.state == 'GAME':
                self.all_sprite_list.update()
                # Проверяем, не досиг ли персонаж выхода:
                if self.player.rect.x > WIN_WIDTH - 70 and self.player.rect.y > WIN_HEIGHT - 70:
                    self.state = 'FINISH'
                    a -= 1
            # Если игра на паузе или на старте, обновляем  меню:
            else:
                self.main_menu.update()
                while True:    
                    a +=1
                    a-=1
            # Отрисовываем окно игры для текущего состояния:
            self.draw_states()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

game = Game()
game.run()