import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale (pygame.image.load('graphics/meeple.PNG').convert_alpha(), (100, 100))
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravityspeed = 0
        self.NumJumpAv = 1
    def player_input(self):
        tasto = pygame.key.get_pressed()
        # Commands
        if tasto[pygame.K_a]:
            self.rect.move_ip(-20, 0)
        elif tasto[pygame.K_d]:
            self.rect.move_ip(20, 0)
        elif tasto[pygame.K_w] and self.NumJumpAv > 0:
            self.gravityspeed = -22
            self.NumJumpAv -= 1
    def apply_gravity(self):
        self.gravityspeed += 1
        self.rect.y += self.gravityspeed
        if self.rect.bottom > ground:
            self.gravityspeed = 0
            self.NumJumpAv = TotJump
            self.rect.bottom = ground
    def update(self):
        self.apply_gravity()
        self.player_input()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 0:
            self.image = pygame.transform.scale(pygame.image.load('graphics/tank.JPG').convert_alpha(), (80, 35))
            y_pos = ground
        else:
            self.image = pygame.transform.rotozoom(pygame.image.load("graphics/dice.png").convert_alpha(), 0, 0.15)
            y_pos = ground - 200

        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    def movement(self):
        self.rect.x += -6

    def destroy(self):
        if self.rect.x < -50:
            self.kill()
    def update(self):
        self.movement()
        self.destroy()

def obstacle_movm():
    if obst_list:   # not empty
        for item in obst_list:
            item.x += -5
            screen.blit(dice_surf,item)
        return [obstacles for obstacles in obst_list if obstacles.right  > 0]
    else:
        return []

def score():
    current_score = (pygame.time.get_ticks() - start_time)//1000
    score_txt = font.render(f'Score: {current_score}', False, (0,0,0))
    score_rect = score_txt.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
    screen.blit(score_txt, score_rect)
    return current_score

def collisions_stop_game():
    if obst_list:
        for rectangle in obst_list:
            if meeple_rect.colliderect(rectangle):
                return False
    return True
def collision_sprite():
    if pygame.sprite.spritecollide(gruppo1.sprite, obst_group, True):
        return False
    else:
        return True


pygame.init()
run = True
game_active = False
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
final_score = 0
start_time = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Super Carcassonne Bros')
clock = pygame.time.Clock()

gruppo1 = pygame.sprite.GroupSingle()
gruppo1.add(Player())
obst_group = pygame.sprite.Group()


#obastcles and timers
obst1 = pygame.USEREVENT + 1
pygame.time.set_timer(obst1, 1600)
#obst_list = []





#GRAVITY
gravityspeed = 0
ground = SCREEN_HEIGHT//6*5
TotJump = 1
NumJumpAv = 2

#OBJECTS
lotr = pygame.transform.scale(pygame.image.load('graphics/Fellowship_footer-bg-fellowship.svg').convert_alpha(),(500,100))
meeple_surf = pygame.transform.scale (pygame.image.load('graphics/meeple.PNG').convert_alpha(), (100, 100))

meeple_rect = meeple_surf.get_rect(midbottom = (200, 200))


#Text
font = pygame.font.Font("graphics/Pixeltype.ttf", 50)
textfont = font.render('Score', False, (200, 200, 200))
text_rect = textfont.get_rect(midtop = (SCREEN_WIDTH/2,100))
text_GO = pygame.font.Font("graphics/Pixeltype.ttf", 100).render(      """Game Over""", False, (200, 0, 0))
text_GO_rect = text_GO.get_rect(center = (SCREEN_WIDTH/2,180))
text_NG = font.render('N - New Game', False, "White")
text_NG_rect = text_NG.get_rect(center = (SCREEN_WIDTH/2,350))
text_Q = font.render('Q - Quit', False, "White")
text_Q_rect = text_Q.get_rect(center = (SCREEN_WIDTH/2,450))




while run:
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            run = False

        if event.type == obst1 and game_active:
            obst_group.add(Obstacle(randint(0,2)))



    if game_active:
        screen.fill((94, 129, 162))
        terr_rect = pygame.draw.line(screen, (120, 50, 50), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_HEIGHT-ground)*2)

        screen.blit(textfont, text_rect)

    #All Sprites
        #obst_list = obstacle_movm()
        gruppo1.draw(screen)
        gruppo1.update()
        obst_group.draw(screen)
        obst_group.update()



        game_active = collision_sprite()


        final_score = score()
    else:
        #obst_list.clear()
        obst_group.empty()
        screen.fill((50,0,50))
        meeple_rect.midbottom = (120, ground)

        screen.blit(text_NG,text_NG_rect)
        screen.blit(text_Q, text_Q_rect)



        if final_score != 0:
            text_final = font.render(f'Final Score:  {final_score}', False, (200, 200, 200))
            text_final_rect = text_final.get_rect(center=(SCREEN_WIDTH / 2, 550))
            screen.blit(text_final, text_final_rect)
            screen.blit(text_GO, text_GO_rect)

        tasto = pygame.key.get_pressed()
        if tasto[pygame.K_n]:
            #tank_rect.left = SCREEN_WIDTH
            game_active = True
            start_time = pygame.time.get_ticks()
        elif tasto[pygame.K_q]:
            run = False
    pygame.display.update()
    clock.tick(60)  # max frame rate
pygame.quit()
