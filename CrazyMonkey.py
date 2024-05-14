import pygame as pg
import math
import random

WIDTH, HEIGHT = 1000, 750
WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Crazy Monkey")

pg.font.init()
BACKGROUND = pg.image.load("Backgrounds.jpg").convert_alpha()
MONKEY = pg.image.load("monkey.png").convert_alpha()
LION = pg.image.load("lion.png").convert_alpha()
START = pg.image.load("start.png").convert_alpha()
EXIT = pg.image.load("arrow.png").convert_alpha()
HELP_B = pg.image.load("question-mark.png").convert_alpha()
Up_Button= pg.image.load("up-arrow.png").convert_alpha()
Left_Button = pg.image.load("left.png").convert_alpha()
Right_Button = pg.image.load("right-arrow.png").convert_alpha()
BACKGROUND2 = pg.image.load("Green.jpg").convert_alpha()
LOGO = pg.image.load("crazy_monkey_logo.png").convert_alpha()
PAUSE_BUTTON = pg.image.load("pause-button.png").convert_alpha()


# Fruit transform and stable location

BANANA = pg.image.load("banana.png").convert_alpha()
imagesize = (80, 80)
BANANA = pg.transform.scale(BANANA, imagesize)
BANANAlocation = [200, 400 , 80, 80]
banana_rect=BANANA.get_rect()

APPLE = pg.image.load("apple.png").convert_alpha()
imagesize2 = (50, 50)
APPLE = pg.transform.scale(APPLE, imagesize2)
APPLElocation = [100, 218, 50, 50]
apple_rect=APPLE.get_rect()

# Set Time For Speed of the Player
clock=pg.time.Clock()
FPS=60

# Transform monkey
width_m = MONKEY.get_width()
height_m = MONKEY.get_height()

#For player Moves and player requirements 
class Player():
    def __init__(self, x, y):
        self.image = pg.transform.scale(MONKEY, (width_m-400, height_m-400))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.flip = False
        self.velocity_y = 0
        self.jump = False

    # Moves / Keys
    def moves(self):
        # For Edges
        edge_x=0
        edge_y=0

        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            edge_x = -15
            self.flip = True
        if keys[pg.K_RIGHT]:
            edge_x = 15
            self.flip = False
        if keys[pg.K_UP] and self.jump == False:
             edge_y = -30
             self.jump = True
        if keys[pg.K_UP] :
             self.jump = False
        
    
        # Gravity(for not lose the player)
        self.velocity_y += 1
        if self.velocity_y > 10:
             self.velocity_y = 10
        edge_y += self.velocity_y

         #Player don't get off the egde off the window
        if self.rect.left + edge_x < 0:
                edge_x = -self.rect.left 
        if self.rect.right + edge_x > WIDTH:
                 edge_x = WIDTH - self.rect.right
        

        # Check if the player is going out of the screen's height
        if self.rect.top + edge_y < 0:
            edge_y = -self.rect.top
        if self.rect.bottom + edge_y > HEIGHT:
            edge_y = HEIGHT - self.rect.bottom
          
        #Ypdate the position of the player when it moves
        self.rect.x += edge_x
        self.rect.y += edge_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            edge_y = 0


    def draw(self):
        WINDOW.blit(pg.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))
    
     # Resets the position of the player after the collision
    def reset_position(self):
        self.rect.x = 100  # Default X coordinates
        self.rect.y = 400  # Default Y coordinates

#To draw player and enemy  through the game window
monkey = Player(100, 400)
monkey_rect = pg.Rect((100, 400, 50, 50))
lion_rect = pg.Rect((400, 400, 50, 50))

# Buttons for Main Menu
class Buttons(): 
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def drawing(self):
        change = False
        position = pg.mouse.get_pos()

        # For the user to tap multiple times on the icons
        if self.rect.collidepoint(position):
            if pg.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                change = True

        if pg.mouse.get_pressed()[0] == 0 :
            self.click = False 
           

        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

        return change
#The buttons that the appear through the windows
st_button = Buttons(400, 200, START)
ex_button = Buttons(900, 650, EXIT)
help_button = Buttons(10, 650, HELP_B)
pause_button = Buttons(900, 10, PAUSE_BUTTON)

# Pause the game after the user taping the pause button and after can continue to play or can exit from the game
def paused():

    pause = True 
    font = pg.font.Font('freesansbold.ttf', 32)
    message = font.render('PAUSED', True, (255, 255, 255))
    message2 = font.render('Press the SPACE button to continue', True, (255, 255, 255) )
    message3 = font.render('Press the ESCAPE button to exit from the game',True, (255, 255, 255))
    messagerect = message.get_rect()
    message2rect= message2.get_rect()
    message3rect = message3.get_rect()
    messagerect.center = 500 , 100
    message2rect.center = 500 , 300
    message3rect.center = 500 , 350

    while pause:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pause = False
                elif event.key == pg.K_ESCAPE:
                    pg.QUIT()
                    quit()

            WINDOW.blit(message,messagerect)
            WINDOW.blit(message2,message2rect)
            WINDOW.blit(message3,message3rect)
        pg.display.update()
# The message that appears on screen when player collides with enemy and the user has the option to start again or to exit the game
def collision():

    font = pg.font.Font('freesansbold.ttf', 32)
    message1 = font.render(' YOU LOST ', True, (255, 255, 255))
    message2 = font.render('Press the space button to start again', True, (255, 255, 255))
    message3 = font.render('Press the ESCAPE button to exit', True, (255, 255, 255))
    message1rect = message1.get_rect()
    message2rect = message2.get_rect()
    message3rect = message3.get_rect()
    message1rect.center = 500, 100
    message2rect.center = 500, 300
    message3rect.center = 500, 350

   
    pause = True
    
    while pause:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    main()
                elif event.key == pg.K_ESCAPE:
                    pg.QUIT()
                    quit()

        WINDOW.blit(message1,message1rect)
        WINDOW.blit(message2,message2rect)
        WINDOW.blit(message3,message3rect)
            
        pg.display.update()

# To show the points that the user have catched during his play
def score(points):
    
    font = pg.font.Font('freesansbold.ttf',32)
    text = font.render("Score : {}".format(points),True, (255, 255, 255), (0, 0, 0))
    textrect = text.get_rect()
    textrect.center= 1000 // 2, 50
    WINDOW.blit(text,textrect)
    
# The messages that it shows when the user reaches 200 points and the user has the option to start again or to exit the game
def finalscore():

    font = pg.font.Font('freesansbold.ttf',32)
    text2 = font.render("You WON!!", True, (255, 255, 255), (0, 0, 0))
    text2rect = text2.get_rect()
    text2rect.center = 500, 100
    text3 = font.render("Press SPACE to play again", True, (255, 255, 255), (0, 0, 0))
    text3rect= text3.get_rect()
    text3rect.center = 500, 300
    text4= font.render("Press the ESCAPE button to exit from the game", True, (255, 255, 255), (0, 0, 0))
    text4rect = text4.get_rect()
    text4rect.center = 500, 350
    pause = True
    
    while pause:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    main()
                elif event.key == pg.K_ESCAPE:
                    pg.QUIT()
                    quit()

        
        WINDOW.blit(text2,text2rect)
        WINDOW.blit(text3,text3rect)
        WINDOW.blit(text4,text4rect)
            
        pg.display.update()


# Main Menu Page for the user to shoose if he wants to play or to read the game's manual
def main_menu():
    run = True

    while run:

        WINDOW.blit(BACKGROUND,(0, 0))
        WINDOW.blit(LOGO,(200, 0))
        
        if st_button.drawing():
            main()
        if help_button.drawing():
            option_page()
        if ex_button.drawing():
            exit()
        
        for event in pg.event.get():

         if event.type == pg.QUIT:
                run = False

        pg.display.update()

# Page for the Manual Page
def option_page():
    run = True
 
    font = pg.font.Font('freesansbold.ttf', 32)
    font2 = pg.font.Font('freesansbold.ttf', 48)
    text = font2.render('How to play', True, (0, 0, 0))
    text2 = font.render('Press the UP arrow key to jump',True, (0, 0, 0))
    text3 = font.render('Press the RIGHT arrow key to move to the right',True,(0, 0, 0))
    text4 = font.render('Press the LEFT arrow key to move to the left',True,(0, 0, 0))
    text5 = font.render('Press the EXIT button to go back to the main menu',True,(0, 0, 0))
    text5rect = text5.get_rect()
    text3rect=text3.get_rect()
    text4rect=text4.get_rect()
    text2rect=text2.get_rect()
    textrect = text.get_rect()
    textrect.center = 500 , 50
    text2rect.center = 410, 200
    text3rect.center = 530, 350
    text4rect.center = 500, 500
    text5rect.center = 500, 700

    while run:

        WINDOW.blit(BACKGROUND2,(0, 0))
        WINDOW.blit(text,textrect)
        WINDOW.blit(text2,text2rect)
        WINDOW.blit(Up_Button, (20, 150))
        WINDOW.blit(text3,text3rect)
        WINDOW.blit(text4,text4rect)
        WINDOW.blit(Right_Button, (20, 300))
        WINDOW.blit(Left_Button, (20, 450))
        WINDOW.blit(text5,text5rect)

        if ex_button.drawing():
           main_menu()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()


        pg.display.update()

# Game Page 
def main():
    game_over = False
    run = True
 
    scrolling = 0
    tiles = math.ceil(WIDTH / BACKGROUND.get_width()) + 2
    moving = 1
    points = 0

    # Variables for timer
    done = False
    miliseconds = 0
    seconds = 0
    minutes = 0
    hour = 0
    lion_posx = WIDTH - 600

    font = pg.font.Font('freesansbold.ttf',32)
    text = font.render(" TIMER : {}:{}:{}:{}".format(hour, minutes, seconds, miliseconds), True, (255, 255, 255), (0, 0, 0))
    textrect = text.get_rect()
    textrect.center= 250 // 2, 50

    while run:

        # Time For Player's Speed
        clock.tick(FPS)


        miliseconds +=1
        

        if miliseconds == 60:
             miliseconds = 0
             seconds += 1
        if seconds == 60:
             seconds = 0
             minutes += 1
        if minutes == 60:
             minutes = 0
             hour += 1
        text = font.render(" TIMER : {}:{}:{}:{}".format(hour, minutes, seconds, miliseconds), True, (255, 255, 255), (0, 0, 0))


        #player movements
        monkey.moves()

        #background/ What prints on screen
       
        for i in range (tiles):
            WINDOW.blit(BACKGROUND,(i * BACKGROUND.get_width() + scrolling - BACKGROUND.get_width(),0))
        WINDOW.blit(text,textrect)  # For printing time
        # To track the position of the bannana every time in the screen
        BANANAlocation[0]=banana_rect.x
        BANANAlocation[1]=banana_rect.y
        WINDOW.blit(BANANA, tuple(BANANAlocation)) # For banana showing on screen
        # To track the position of the apple every time in the screen
        APPLElocation[0]=apple_rect.x
        APPLElocation[1]=apple_rect.y
        WINDOW.blit(APPLE, tuple(APPLElocation)) # For apple showing on screen
        WINDOW.blit(PAUSE_BUTTON, pause_button)

        #For the enemy (lion) to move towards the  screen and goes to the monkey
        if lion_posx < - 100:
             lion_posx = 1000
        WINDOW.blit(LION,(lion_posx, WIDTH-350))
        lion_posx -= 3
        lion_rect = pg.Rect(lion_posx, 400, 50, 50)

        # To keep the score of the current game
        score(points)


        # Check if the monkey is colliding with the lion
        if monkey.rect.colliderect(pg.Rect(lion_posx, 700, 70, 70)):
            game_over = True

        #The positions of the fruits(Bannana or Apple)will be change when the monkey collides with them 
        if monkey.rect.colliderect(banana_rect):
            banana_rect.x=random.randint(100,900)
            banana_rect.y=random.randint(100,670)
            points += 5
            
        if monkey.rect.colliderect(apple_rect):
            apple_rect.x=random.randint(100,900)
            apple_rect.y=random.randint(100,670)
            points += 3
            

        scrolling -= 4 * moving

        if abs(scrolling) > BACKGROUND.get_width():
             scrolling = 0
        # When the user catches 200 points the game will be over/ Finall score of the game
        if points >= 201:
            run = False
            finalscore()

        if game_over:
            collision()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    monkey.reset_position()  # The monkey returns in her position
                    main()
        #For the game can be paused by user
        if pause_button.drawing():
            paused()
        
        #player drawing on screen
        monkey.draw()
       
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

            # Restart the game by pressing the space button
            if game_over and event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE: 
                    main()
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
 
    #Update image / game
        pg.display.update()

   

main_menu()