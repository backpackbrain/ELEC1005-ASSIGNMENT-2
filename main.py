# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

"""
S: Below is the imports that are needed for the main function of the game
cgitb is a module used to enable traceback tracking in Python scripts
tkinter is a standard python graphical user interface module
turtle involves basic sprite movement in python
thorpy is a graphical module added for user interactions
pygame is a game based module, which involves input from users as seen in the keys imported
pickle is a module used to store variables to disk i.e. high scores
sys is a module which contains useful functions that manage system items such as exiting functions.
game is the other python script which contains the Game class among other relevant functions
"""

from cgitb import grey
from tkinter import N
from turtle import back
import pygame
import thorpy  # S: imported thorpy
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
import pickle  # S: added pickle module for high scores
import sys #S: added sys to fix exit bugs
from game import Game


'''
S: Below are the colours used in the game, set as pygame.Color variables using RGB formatting
'''
black = pygame.Color(0, 0, 0)
# add game background
gamebackground = pygame.Color(124, 194, 72)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)
gray = pygame.Color(80, 80, 80)

'''
S: Below is the initialisation of the game via calling the Game class, and setting the length 
of the snake rectangle as well as initialising the snake controlled by the Snake class
and initialising them with the pygame.init() call. the fpsClock is linked to the passage of time and thus 
the speed of the game is linked how fast the game runs per second of real time.
The background is filled and the intro screen which displays Gluttonous, the game title, is set.
'''
game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
# T. create the screen/ can be modified bigger
screen = pygame.display.set_mode(
    (game.settings.width * 15, game.settings.height * 15))
# added background as new way to fill the UI
background = pygame.Surface(
    (game.settings.width * 15, game.settings.height * 15))
background.fill((0, 0, 100))
pygame.display.set_caption('Gluttonous')

# *******************************************************************


thorpy.theme.set_theme('human')
line = thorpy.Line(400, 'h')
menu = thorpy.Menu()
# [Sharang: trying out thorpy for GUI element addition. Above is a test slider and below is initialising it, go to thorpy documentation to understand better]
#S: These are now legacy elements that simply add to the UI but do not have functionality with regards to difficulty which the above comment would imply
for element in menu.get_population():
    element.surface = screen


crash_sound = pygame.mixer.Sound('./sound/crash.wav')#S: This is the noise that plays when a player crashes their snake.

'''
S: The below function renders a given text string onto a text surface in pygame and returns the relevant text surface
along with the rectangle it should be contained in.
'''
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

'''
S: The below function takes text and coordinates and uses the text_objects function to display that text at the given 
position and at a given font size.
'''
def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)

    # pygame.display.update()  # solved for blink bug on the front page

# S: Duplicated message_display in order to use a separate function to display the crash score when the player loses with slightly different variables
#The functionality is identical to the original


def message_display_crash(text, x, y, color=black):
    # S: Smaller font than the original
    large_text = pygame.font.SysFont('comicsansms', 20)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

'''
S: The below function uses pygame functionality such as mouse.get_pos() to set up a button in pygame which displays
a given message at a given coordinate with a given width and height, with different colours when the buttons are active
or inactive. It changes the colour when the mouse is over the button, and if it is clicked, then it executes any parameter
that is given (such as the game loop for the start button or the quitgame function for the quit button)
'''
def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)

#S: A simple function that quits pygame scripts and python scripts when called.
def quitgame():
    pygame.quit()
    sys.exit(0)#S: replaced quit with sys.exit to prevent for errors when exiting the game normally

# ***************************************************************** new-page (level)


def level_page():
    screen.fill(gray)
    pygame.draw.rect(screen, gray, (200, 150, 100, 50))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)#S: added to fix error bug on X button in window being clicked
            menu.react(event)

        message_display('Choose level', game.settings.width /
                        2 * 15, game.settings.height / 4 * 15)
        button('easy', 50, 200, 60, 40, yellow,
               bright_yellow, game_loop, {"speed": 15})
        button('medium', 170, 200, 80, 40,
               blue, bright_blue, game_loop,  {"speed": 20})
        button('hard', 300, 200, 60, 40, red,
               bright_red, game_loop,  {"speed": 25})

        pygame.display.flip()
        pygame.time.Clock().tick(15)

# *****************************************************************


#S: As this function was modified, it is thoroughly commented; it handles the events when a player's snake crashes.
def crash():
    pygame.mixer.Sound.play(crash_sound)#S: plays the crash audio file
    screen.blit(background, (0, 0))#S: displays a different background after crashing
    # S: added crashscore to print to player the score they got in string form
    crashscore = str(game.snake_score())
    try:
        with open('highscores.dat', 'rb') as file:  # S: opens any existing high scores
            highscores = pickle.load(file)
    except:
        # S: minimum of three scores for the top three to prevent errors in access
        highscores = [0] * 3
    '''
    S: Using the pickle method of storing the high scores as an array, the above code loads the existing
    high scores unless there are none, in which case the array is turned into three zeroes 
    '''
    highscores.append(
        game.snake_score())  # S: appends the current score to the list of high scores
    # S: sorts the high scores from highest to lowest
    highscores = sorted(highscores, reverse=True)

    # S: added crashstring to print to player with good formatting
    crashstring = 'Crashed: Your score was ' + crashscore
    # S: replaced original string with crashstring, calling the duplicated function
    message_display_crash(crashstring, game.settings.width /
                          2 * 15, game.settings.height / 3 * 15, white)
    message_display_crash("TOP THREE BEST SCORES", game.settings.width / 2 *
                          15, game.settings.height / 3 * 18, white)  # S: heading of scoreboard
    # S: accessing sorted array to find first place score
    firststring = '#1: ' + str(highscores[0])
    # S: accessing sorted array to find second place score
    secondstring = '#2: ' + str(highscores[1])
    # S: accessing sorted array to find third place score
    thirdstring = '#3: ' + str(highscores[2])
    message_display_crash(firststring, game.settings.width / 2 * 15,
                          game.settings.height / 3 * 21, white)  # S: displaying first place score
    message_display_crash(secondstring, game.settings.width / 2 * 15,
                          game.settings.height / 3 * 24, white)  # S: displaying second place score
    message_display_crash(thirdstring, game.settings.width / 2 * 15,
                          game.settings.height / 3 * 27, white)  # S: displaying third place score
    # S: stores the high score array in the file so that it is stored on disk and not just when the program is executed
    with open('highscores.dat', 'wb') as file:
        pickle.dump(highscores, file)

    time.sleep(5)  # S: made the text stay longer on screen
    game.snake.initialize()#S: made snake position reset before the interface is called again, solving the repeat-crash bug
    initial_interface()#S: loads the initial interface after the time has passed


'''
S: The below function defines the initial interface for the game, or the intro, and checks if the quit button is called and quits if so.
The go and quit buttons are initiated with the button function, and the title is displayed with the message_display function.
The screen is then loaded using the pygame display and time functions, and it remains stable until a button is clicked.
'''
def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)#S: added to fix error bug on X button in window being clicked
            # S: thorpy ui code, [which will be used later with variable set by user]
            #S: This is now purely cosmetic
            menu.react(event)

        # S: this is the background variable as earlier used, to improve how the screen is displayed
        screen.blit(background, (0, 0))

        message_display('Gluttonous', game.settings.width /
                        2 * 15, game.settings.height / 4 * 15)

        button('Go!', 80, 240, 80, 40, green, bright_green, level_page)
        button('Quit', 270, 240, 80, 40, red, bright_red, quitgame)

        pygame.display.flip()
        pygame.time.Clock().tick(15)


"""
S: The game loop function, which has been modified by Tien, runs the functions related to movement of the snake and visual
graphics of the snake, as well as placing the strawberry items on the screen via calling the relevant game functions from 
the other python script, and calling crash() if the game has ended.
"""
def game_loop(player, fps=10):  # fps start with 10
    speed = 0
    try:

        # Tien. added a variable for fps to edit the speed,
        speed = player["speed"]
    except:
        speed = fps
    game.restart_game()

    while not game.game_end():

        pygame.event.pump()

        move = human_move()

        if(game.do_move(move) == 1):  # Tien. speed increase when the score increases
            # Tien. if statement added, to method "do_move" (whenever it returns to 1(scores)) fps increment by 5
            speed += 0.8

        screen.fill(gamebackground)
        # add game background
        # can be change through gamebackground

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(speed)  # switch parameter (from (fps) to (speed)

    crash()

'''
S: This function accepts the key down input from the player and transforms it into string variables to return to the
game loop so that it can appropriately move the snake with the game script's functions. 
'''
def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)#S: added to fix error bug on X button in window being clicked

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move

#S: Runs the python script from the initial interface function if it is called by the name of its own function.
if __name__ == "__main__":
    initial_interface()
