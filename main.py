import pygame
import os

#render font on the screen
pygame.font.init()
#init sound effect
pygame.mixer.init()
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("apple game <3")

# set color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255 ,0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
PURPLE =  (0,32,128)

BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)  # for setting boarder for obj movement

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('sounds','hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('sounds','fire.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

FPS = 60
VEL = 5 #move speed
BULLET_VEL = 7
MAX_BULLETS = 10
IMG_W, IMG_H = 60, 60

# create custom user event
LUCA_HIT = pygame.USEREVENT +1
LUMI_HIT = pygame.USEREVENT +2


# load the image
LUCA_IMG_RAW = pygame.image.load(os.path.join('pic','luca.png'))
# resize luca img and rotate:here rotate 360==no rotate
LUCA_IMG = pygame.transform.rotate(
    pygame.transform.scale(LUCA_IMG_RAW,(IMG_W,IMG_H))
    ,360)
LUMI_IMG_RAW = pygame.image.load(os.path.join('pic','lumi.png'))
LUMI_IMG = pygame.transform.scale(LUMI_IMG_RAW,(IMG_W*2,IMG_H*2))
    
#let background fit to the screen
SPACE = pygame.transform.scale( pygame.image.load(os.path.join('pic','bg.jpg')),(WIDTH,HEIGHT))


def draw_window(lucaobj, lumiobj, luca_bullets, lumi_bullets,  luca_health, lumi_health): 
    WIN.blit(SPACE,(0,0)) # because is the backgound can start from top letft 
    # WIN.fill(WHITE)    fill screen with white
    # there's a sequence for put things onto screen, fill the screen first then start placing thing on
    # pygame start from letupper corner(0,0)

    pygame.draw.rect(WIN, BLACK, BORDER) # draw a line in the middle
    
    lumi_health_text= HEALTH_FONT.render("Health: " + str(lumi_health), 1, PURPLE) 
    # 1 is anti aliasing, no need to understand, white is for the font color
    luca_health_text= HEALTH_FONT.render("Health: " + str(luca_health), 1, PURPLE) 
    
    WIN.blit(lumi_health_text, (WIDTH - lumi_health_text.get_width()-10,10 ))
    WIN.blit(luca_health_text, (10, 10))

    WIN.blit(LUCA_IMG,(lucaobj.x, lucaobj.y)) # draw a blit to put things
    WIN.blit(LUMI_IMG,(lumiobj.x, lumiobj.y))



    for bullet in lumi_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in luca_bullets:
        pygame.draw.rect(WIN,BLUE,bullet)

    pygame.display.update()   

def luca_move_handler(keys_pressed, lucaobj):
    if keys_pressed[pygame.K_a] and lucaobj.x - VEL > 0:  # LEFT
        lucaobj.x -= VEL
    if keys_pressed[pygame.K_d] and lucaobj.x + VEL + lucaobj.width < BORDER.x:  # RIGHT
        lucaobj.x += VEL
    if keys_pressed[pygame.K_w] and lucaobj.y - VEL > 0:  # UP
        lucaobj.y -= VEL
    if keys_pressed[pygame.K_s] and lucaobj.y + VEL + lucaobj.height < HEIGHT - 15:  # DOWN
        lucaobj.y += VEL

def lumi_move_handler(keys_pressed, lumiobj):
    if keys_pressed[pygame.K_LEFT] and lumiobj.x - VEL > BORDER.x + BORDER.width:  # LEFT
        lumiobj.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and lumiobj.x + VEL + lumiobj.width < WIDTH:  # RIGHT
        lumiobj.x += VEL
    if keys_pressed[pygame.K_UP] and lumiobj.y - VEL > 0:  # UP
        lumiobj.y -= VEL
    if keys_pressed[pygame.K_DOWN] and lumiobj.y + VEL + lumiobj.height < HEIGHT - 15:  # DOWN
        lumiobj.y += VEL

def handle_bullets(luca_bullets,lumi_bullets, lucaobj, lumiobj):
    for bullet in luca_bullets:
        bullet.x +=BULLET_VEL
        if lumiobj.colliderect(bullet): #check two rect collid
            # posting the custom event, adding the event to the get.event() queue
            pygame.event.post(pygame.event.Event(LUMI_HIT)) 
            luca_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            luca_bullets.remove(bullet)
    for bullet in lumi_bullets:
        bullet.x -=BULLET_VEL
        if lucaobj.colliderect(bullet): #check two rect collid
            pygame.event.post(pygame.event.Event(LUCA_HIT))
            lumi_bullets.remove(bullet)
        elif bullet.x < 0:
            lumi_bullets.remove(bullet)

def draw_winner(text) :
    draw_text = WINNER_FONT.render(text, 1, RED)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2 , HEIGHT//2-draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(3000) # dealy 5 sec and continue

def main():
    lucaobj = pygame.Rect(100,300, IMG_W, IMG_H)
    lumiobj = pygame.Rect(700,300, IMG_W*2, IMG_H*2)

    luca_bullets = []
    lumi_bullets = []

    luca_health = 10
    lumi_health = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # control the speed fps = 60
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(luca_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(lucaobj.x + lucaobj.width, lucaobj.y + lucaobj.height//2-2, 10, 5)
                    luca_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
                if event.key == pygame.K_RCTRL and len(lumi_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        lumiobj.x, lumiobj.y + lumiobj.height//2 - 2, 10, 5)
                    lumi_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    #BULLET_FIRE_SOUND.play()
        
            if event.type == LUMI_HIT:
                lumi_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == LUCA_HIT:
                luca_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if lumi_health <= 0 :
            winner_text = "luca wins"
        
        if luca_health <=0 :
            winner_text = "lumi wins"
        
        if winner_text !="" :
            draw_winner(winner_text) # someone won
            break

        keys_pressed = pygame.key.get_pressed() #which key current pressed down
        luca_move_handler(keys_pressed,lucaobj)
        lumi_move_handler(keys_pressed,lumiobj)

        handle_bullets(luca_bullets,lumi_bullets, lucaobj, lumiobj)
        
        draw_window(lucaobj, lumiobj, luca_bullets, lumi_bullets, luca_health, lumi_health)
    
    main()

if __name__ =="__main__":
    main()    