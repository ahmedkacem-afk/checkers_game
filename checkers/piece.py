from .constants import SQUARE_SIZE,lighter_color,CROWN,BLACK,WHITE
import pygame

class Piece:
    PADDING=8
    outline=8
    def __init__(self,row,col,color):
        self.color = color
        self.row = row
        self.col = col
        self.king = False
        
        self.x=0
        self.y=0
        self.calc_pos()
    def move(self,row,col):
        self.row=row
        self.col=col
        self.calc_pos()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2
    def make_king(self):
        if self.row == 0 and self.color ==BLACK:
            self.king = True
        elif self.row == 7 and self.color == WHITE:
            self.king = True
        else:
            return self.king
            
    def draw(self,win):
        radius=SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win,self.color,(self.x,self.y),radius)
        pygame.draw.circle(win,lighter_color(self.color),(self.x,self.y),radius-self.outline)
        if self.king:
            win.blit(CROWN,((self.x - CROWN.get_width()//2),(self.y - CROWN.get_height()//2)))

    
    
    
    
    def __repr__(self):
        return str(f"({self.row},{self.col})")
