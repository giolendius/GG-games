import pygame
from random import randint

pygame.init()
run = True
game_active = False
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Super Carcassonne Bros')
clock = pygame.time.Clock()
final_score = 0
start_time = 0



#obastcles and timers
obst1 = pygame.USEREVENT + 1
obst2 = pygame.USEREVENT + 2
pygame.time.set_timer(obst1, 1600)
pygame.time.set_timer(obst2, 2000)
obst_list = []

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



#GRAVITY
gravityspeed = 0
ground = SCREEN_HEIGHT//6*5
TotJump = 1
NumJumpAv = 2

#OBJECTS
lotr = pygame.transform.scale(pygame.image.load('graphics/Fellowship_footer-bg-fellowship.svg').convert_alpha(),(500,100))
meeple_surf = pygame.transform.scale (pygame.image.load('graphics/meeple.PNG').convert_alpha(), (100, 100))
#meeple_surf.fill((250, 0, 0 ))
meeple_rect = meeple_surf.get_rect(midbottom = (200, 200))

tank_surf = pygame.transform.scale(pygame.image.load('graphics/tank.JPG').convert_alpha(), (80,35))
dice_surf = pygame.transform.rotozoom(pygame.image.load("graphics/dice.png").convert_alpha(), 0,0.15)


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
            if randint(0,2)==0:
                obst_list.append(tank_surf.get_rect(bottomleft = (randint(SCREEN_WIDTH, SCREEN_WIDTH+200), ground)))
        #if event.type == obst2 and game_active:
            else:
                obst_list.append(dice_surf.get_rect(center = (randint(SCREEN_WIDTH, SCREEN_WIDTH+100), ground)))

    tasto = pygame.key.get_pressed()

    if game_active:
        screen.fill((94, 129, 162))

        #circ = pygame.draw.circle(screen, "Red", ball_rect.center, ball_rect.width//2)
        #ball_rect.x += 4
        #ball_rect.y += 4

        terr_rect = pygame.draw.line(screen, (120, 50, 50), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_HEIGHT-ground)*2)
        #screen.blit(lotr, (-100, 100))
        screen.blit(textfont, text_rect)

    #OBSTACLES
        obst_list = obstacle_movm()

    #TANK OLD
     #   screen.blit(tank_surf, tank_rect)
     #   tank_rect.left += -4
     #   if tank_rect.right < 0:
     #       tank_rect.left = SCREEN_WIDTH

    #Meeple
        screen.blit(meeple_surf, meeple_rect)
        meeple_rect.y += gravityspeed
        gravityspeed += 1
        if meeple_rect.bottom > ground:
            gravityspeed = 0
            NumJumpAv = TotJump
            meeple_rect.bottom = ground

    #Commands
        if tasto[pygame.K_a]:
            meeple_rect.move_ip(-20, 0)
        elif tasto[pygame.K_w] and NumJumpAv > 0:
            gravityspeed = -22
            NumJumpAv -= 1
        elif tasto[pygame.K_d]:
            meeple_rect.move_ip(20, 0)

        game_active = collisions_stop_game()
        final_score = score()
    else:
        obst_list.clear()
        screen.fill((50,0,50))
        meeple_rect.midbottom = (120, ground)

        screen.blit(text_NG,text_NG_rect)
        screen.blit(text_Q, text_Q_rect)



        if final_score != 0:
            text_final = font.render(f'Final Score:  {final_score}', False, (200, 200, 200))
            text_final_rect = text_final.get_rect(center=(SCREEN_WIDTH / 2, 550))
            screen.blit(text_final, text_final_rect)
            screen.blit(text_GO, text_GO_rect)


        if tasto[pygame.K_n]:
            #tank_rect.left = SCREEN_WIDTH
            game_active = True
            start_time = pygame.time.get_ticks()
        elif tasto[pygame.K_q]:
            run = False
    pygame.display.update()
    clock.tick(120)  # max frame rae
pygame.quit()
