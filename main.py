import pygame
from checkers.constants import WIDTH, HEIGHT
from checkers.board import Board
from checkers.game import Game
import random as rd
FPS=60
WIN= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Checkers')


def main():
    run=True
    game=Game(WIN)
    clock = pygame.time.Clock()
    piece1=game.board.get_piece(2,5)
    piece2=game.board.get_piece(1,4)
    piece3=game.board.get_piece(5,2)
    piece1.king=True
    game.board.move(piece2,4,1)
    game.board.move(piece3,3,2)
    game.update()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if game.board.winner()!=None :
                print(game.winner())
                run=False
            
                
                   
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                row,col=game.board.get_row_col_from_mouse(pos)
                piece=game.board.get_piece(row,col)
                
                
                
                game.select(row,col)
               
        game.update()
    pygame.quit()
    
main()

    