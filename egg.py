import pygame,time
from pygame.locals import * # Basic pygame imports
import random
import os
import sys # We will use sys.exit to exit the program

pygame.mixer.init()

pygame.init()
prevtime=time.time()

score = 0

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 1000
screen_height = 600
SCREEN = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("bg.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

#Other Images
egg = pygame.image.load('egg.png').convert_alpha()
foul = pygame.image.load('foul.png').convert_alpha()
bonus = pygame.image.load('bonus.png').convert_alpha()
basket = pygame.image.load('basket.png').convert_alpha()
hen = pygame.image.load('hen.png').convert_alpha()

#Images Heights
eggh = egg.get_height()
foulh = foul.get_height()
bonush = bonus.get_height()
basketh = basket.get_height()
henh = hen.get_height()

#Images Widths
eggw = egg.get_width()
foulw = foul.get_width()
bonusw = bonus.get_width()
basketw = basket.get_width()
henw = hen.get_width()

# initial coordinates
basketx = int(screen_width/2)
baskety = screen_height - 120
henx = 20
heny = 0
eggx = henw/2
eggy = henh


# Game sounds
die = pygame.mixer.Sound('audio/die.wav')
hit = pygame.mixer.Sound('audio/hit.wav')
point = pygame.mixer.Sound('audio/point.wav')
swoosh = pygame.mixer.Sound('audio/swoosh.wav')
wing = pygame.mixer.Sound('audio/wing.wav')



# Game Title
pygame.display.set_caption("Save Eggs")
pygame.display.update()
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    SCREEN.blit(screen_text, [x,y])
	

def collide(egglistx,egglisty,foullistx,foullisty,bonuslistx,bonuslisty):
	global score
	temp = 0 

	for x,y in zip(egglistx,egglisty):
		if basketx<=x+eggw/2<=basketx+basketw and y+eggh<=baskety<=y+eggh+3 :
			score+=1
			point.play()
		elif screen_height-5<=y<=screen_height :
			temp+=1

	for x,y in zip(foullistx,foullisty):
		if basketx<=x+foulw/2<=basketx+basketw and y+foulh<=baskety<=y+foulh+3 :
			score-=1
			point.play()

	for x,y in zip(bonuslistx,bonuslisty):
		if basketx<=x+bonusw/2<=basketx+basketw and y+bonush<=baskety<=y+bonush+3 :
			temp-=2
			point.play()

	return temp


def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    global score 
    score = 0
    response = 0

    global basketx,baskety,prevtime

    speed = 6
    vx = 0

    egglistx=[]
    egglisty=[]
    foullistx=[]
    foullisty=[]
    bonuslistx=[]
    bonuslisty=[]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RIGHT:
            	vx = speed
            	# wing.play()

            if event.type == KEYDOWN and event.key == K_LEFT:
            	vx = speed * -1
            	# wing.play()


        # collision check
        response += collide(egglistx,egglisty,foullistx,foullisty,bonuslistx,bonuslisty)
        if response>=5:
        	hit.play()
        	text_screen("Game Over", red, 5, 5)
        	text_screen("Your Score "+str(score), red, 25, 55)
        	pygame.display.update()
        	pygame.time.wait(3000)
        	return

        text_screen("Score: " + str(score), red, 5, 5)
        pygame.display.update()
        # clock.tick(fps)

        # move basket left and right
        basketx = basketx + vx

        # restrict basket flow within window
        if basketx<0 :
        	basketx = 0
        if basketx + basketw > screen_width :
        	basketx = screen_width - basketw


        SCREEN.blit(bgimg,(0,0))
        SCREEN.blit(basket,(basketx,baskety))

        tmp=0

        for i in range(5):
            SCREEN.blit(hen,(henx+tmp,heny))
            tmp+=200

        tmp=200


        # eggchoice 
	        # 1 normal egg
	        # 2 foul egg
	        # 3 bonus egg
       	choice=5
       	eggchoice=0
       	curtime=time.time()
       	if curtime-prevtime>2:
       		prevtime=curtime
       		# choice = random.randint(0, 4)
       		choice = 0
       		choice2 = random.randint(1, 10)
       		if 1<=choice2<=5 :
       			eggchoice=1
       		elif 6<=choice2<=8 :
       			eggchoice=2
       		else:
       			eggchoice=3
       		eggchoice=1


        downvel = 10
        egglisty = [i + downvel for i in egglisty]
        foullisty = [i + downvel for i in foullisty]
        bonuslisty = [i + downvel for i in bonuslisty]


        if choice == 0 :
        	if eggchoice == 1:
	            egglistx.append(eggx)
	            egglisty.append(eggy)
	        elif eggchoice == 2:
	            foullistx.append(eggx)
	            foullisty.append(eggy)
	        else:
	            bonuslistx.append(eggx)
	            bonuslisty.append(eggy)

        elif choice == 1 :
        	if eggchoice == 1:
	            egglistx.append(eggx+tmp)
	            egglisty.append(eggy)
	        elif eggchoice == 2:
	            foullistx.append(eggx+tmp)
	            foullisty.append(eggy)
	        else:
	            bonuslistx.append(eggx+tmp)
	            bonuslisty.append(eggy)

        elif choice == 2 :
        	if eggchoice == 1:
	            egglistx.append(eggx+2*tmp)
	            egglisty.append(eggy)
	        elif eggchoice == 2:
	            foullistx.append(eggx+2*tmp)
	            foullisty.append(eggy)
	        else:
	            bonuslistx.append(eggx+2*tmp)
	            bonuslisty.append(eggy)

        elif choice == 3 :
        	if eggchoice == 1:
	            egglistx.append(eggx+3*tmp)
	            egglisty.append(eggy)
	        elif eggchoice == 2:
	            foullistx.append(eggx+3*tmp)
	            foullisty.append(eggy)
	        else:
	            bonuslistx.append(eggx+3*tmp)
	            bonuslisty.append(eggy)

        elif choice == 4 :
        	if eggchoice == 1:
	            egglistx.append(eggx+4*tmp)
	            egglisty.append(eggy)
	        elif eggchoice == 2:
	            foullistx.append(eggx+4*tmp)
	            foullisty.append(eggy)
	        else:
	            bonuslistx.append(eggx+4*tmp)
	            bonuslisty.append(eggy)


        for x,y in zip(egglistx,egglisty):
        	SCREEN.blit(egg,(x,y))

        for x,y in zip(foullistx,foullisty):
        	SCREEN.blit(foul,(x,y))

        for x,y in zip(bonuslistx,bonuslisty):
        	SCREEN.blit(bonus,(x,y))

        pygame.display.update()
        clock.tick(fps)
    

    pygame.quit()
    quit()

def welcome():
    exit_game = False
    while not exit_game:
        SCREEN.fill((233,210,229))
        text_screen("Aman loves Omelette", black, 260, 250)
        text_screen("Press Space Bar To Save Eggs", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('back.mp3')
                    # pygame.mixer.music.play()
                    return

        pygame.display.update()
        clock.tick(fps)

while 1:
	welcome()
	gameloop()