from random import randint

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.s_x = speed
        self.s_y = 0
        self.rot = 0
        self.u = 4
        self.im = pygame.image.load("graphics/SnakeHead.png").convert_alpha()
        self.image = pygame.transform.scale(self.im, (100, 100))
        self.rect = self.image.get_rect(center=(800, 400))

    def input(self):
        tasto = pygame.key.get_pressed()
        if self.s_y == 0:
            if tasto[pygame.K_UP] and self.u <= 0:
                self.s_x = 0
                self.s_y = -speed
                self.rot = 90
                self.u = 5
            if tasto[pygame.K_DOWN]and self.u <= 0:
                self.s_x = 0
                self.s_y = speed
                self.rot = -90
                self.u = 5
        if self.s_x == 0:
            if tasto[pygame.K_RIGHT]and self.u <= 0:
                self.s_x = speed
                self.s_y = 0
                self.rot = 0
                self.u = 5
            if tasto[pygame.K_LEFT]and self.u <= 0:
                self.s_x = -speed
                self.s_y = 0
                self.rot = 180
                self.u = 5
        self.image = pygame.transform.rotate(pygame.transform.scale(self.im, (100, 100)), self.rot)

    def inputt(self):
        tasto = pygame.key.get_pressed()
        if tasto[pygame.K_UP]:
            self.rect.y = -speed
            self.rot = 90
        if tasto[pygame.K_DOWN]:
            self.rect.y = speed
            self.rot = -90
        if tasto[pygame.K_RIGHT]:
            self.rect.x = speed
            self.rot = 0
        if tasto[pygame.K_LEFT]:
            self.rect.x = -5
            self.rot = 180
        self.image = pygame.transform.rotate(pygame.transform.scale(self.im, (100, 100)), self.rot)

    def movement(self):
        self.rect.move_ip(self.s_x, self.s_y)
        self.u -= 1
        if self.u <=0:
            self.u=0

    def on_a_thorus(self):
        if self.rect.centerx <= 0:
            self.rect.centerx = SCREEN_W - 1
        if self.rect.centerx >= SCREEN_W:
            self.rect.centerx = 0
        if self.rect.centery <= 0:
            self.rect.centery = SCREEN_H - 1
        if self.rect.centery >= SCREEN_H:
            self.rect.centery = 0

    def update(self):
        self.movement()
        self.input()
        self.on_a_thorus()


class Bodypart(pygame.sprite.Sprite):
    def __init__(self, position, length):
        super().__init__()
        self.image = pygame.image.load("graphics/SnakeBody.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=position)
        self.ciccia = length

    def finite_tail(self):
        if len(gruppo_body.sprites()) > self.ciccia:
            self.kill()

    def update(self):
        self.finite_tail()


class Apple(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("graphics/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=position)


class GameState:
    def __init__(self):
        self.state = 'start_screen'
        self.punteggio = 0
        self.initial_length = 20

    def state_manager(self):
        if self.state == "main_game":
            self.main_game()
        if self.state == "start_screen":
            self.start_screen()
        if self.state == "play_again":
            self.play_again()

    def start_screen(self):

        text('N - New Game', (200, 200, 200), 50, (SCREEN_W // 2, 350))
        text("Commands:", (200, 200, 200), 50, (SCREEN_W // 2, 500))
        text("Arrow Keys  - Move Snake", (200, 200, 200), 50, (SCREEN_W // 2, 550))
        tasto = pygame.key.get_pressed()

        if tasto[pygame.K_n]:
            self.state = "main_game"
            # start_time = pygame.time.get_ticks()
        elif tasto[pygame.K_q]:
            run = False


    def main_game(self):
        screen.fill((154, 132, 71))
        gruppo_mele.draw(screen)
        gruppo_body.draw(screen)
        gruppo_player.draw(screen)
        gruppo_body.add(Bodypart(
            (gruppo_player.sprite.rect.centerx,
             gruppo_player.sprite.rect.centery), self.initial_length
            ))
        gruppo_body_col.add(gruppo_body.sprites()[0:self.initial_length - 6])

        gruppo_mele.update()
        gruppo_body.update()
        gruppo_player.update()

        increase = eating_apples()
        self.punteggio += increase * 50
        self.speed = min(0 + int(self.punteggio // 100), 40)
        self.initial_length += increase

        text(f'Score: {self.punteggio}', (200, 200, 200), 50,(SCREEN_W / 2, 100))
        # gruppo_text.draw(screen)

        if death():
            print("morte")
            self.state = "play_again"
            gruppo_body_col.empty()
            gruppo_body_col.empty()
            gruppo_body_col.update()
            gruppo_body_col.update()
            #screen.fill((200, 182, 120))
            pygame.display.update()
            for sprite in gruppo_body.sprites()[:]:
                sprite.kill()


    def play_again(self):

        text("Game Over", "Red", 100, (SCREEN_W//2, 150))
        self.messaggio = ''
        if 100 <= self.punteggio:
            self.messaggio = 'Nice try, but you can do better'
        if 1200 <= self.punteggio:
                self.messaggio = 'Good result!'
        if 4000 <= self.punteggio:
            self.messaggio = 'Amazing!! That was great!'
        text(self.messaggio, (200, 200, 200), 50, (SCREEN_W // 2, 350))
        text('N - New Game', (200, 200, 200), 50, (SCREEN_W // 2, 450))

        self.punteggio = 0
        self.initial_length = 20
        tasto = pygame.key.get_pressed()


        if tasto[pygame.K_n]:
            self.state = "main_game"
            #start_time = pygame.time.get_ticks()
        elif tasto[pygame.K_q]:
            run = False

def text(txt, color, size, posit):
    font = pygame.font.Font("graphics/Pixeltype.ttf", size)
    txtsurf = font.render(txt, False, color)
    text_rect = txtsurf.get_rect(midtop=posit)
    screen.blit(txtsurf, text_rect)


def eating_apples():
    if pygame.sprite.spritecollide(gruppo_player.sprite, gruppo_mele, True):
        gruppo_mele.add(Apple((randint(50, SCREEN_W-50), randint(50, SCREEN_H-50))))
        return length_increase
    else:
        return 0


def death():
    if len(pygame.sprite.spritecollide(gruppo_player.sprite, gruppo_body_col, False)) > 8:
        print(f'{len(pygame.sprite.spritecollide(gruppo_player.sprite, gruppo_body, False))} collided with head')
        return True
    else:
        return False


pygame.init()
SCREEN_W = 1000
SCREEN_H = 800
#initial_length = 20
length_increase = 2
#in_speed = 15
speed = 15
#max_speed = 40
#Score = 0
game_state = GameState()
#body_len = 20
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Python the snake")

gruppo_player = pygame.sprite.GroupSingle()
gruppo_player.add(Player())
gruppo_mele = pygame.sprite.Group()
gruppo_mele.add(Apple((200, 300)))
gruppo_body = pygame.sprite.Group()
gruppo_body_col = pygame.sprite.Group()



run = True
while run:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

    game_state.state_manager()



    pygame.display.update()
    pygame.time.Clock().tick(30)
pygame.quit()
