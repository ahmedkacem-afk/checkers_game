import pygame

WIDTH , HEIGHT = 800,800
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

#rgb colors
RED=(255,0,0)
WHITE=(210,210,210)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREY=(128,128,128)
BROWN=(150,75,0)
LIGHT_BROWN=( 200 , 173 , 127)
def lighter_color(color):
    if color == BLACK:
        return (20,20,20)
    elif color == WHITE:
        return (200,200,200)
    else:
        return color
CROWN=pygame.transform.scale(pygame.image.load('src/checkers/assets/crown.png'),(44,25))