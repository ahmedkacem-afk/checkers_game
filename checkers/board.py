import pygame
from .constants import LIGHT_BROWN,BROWN,ROWS,COLS,RED,SQUARE_SIZE,WHITE,BLACK
from .piece import Piece
import numpy as np
class Board:
    def __init__(self):
        self.board=[]
        self.to_capture=False
        self.double_jump=False
        self.black_left=self.white_left=12
        self.black_kings=self.white_kings=0
        self.create_board()
    def draw_squares(self,win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(win,LIGHT_BROWN,(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col%2 == ((row+1)%2):
                    if row<3:
                        self.board[row].append(Piece(row,col,WHITE))
                    elif row>4 :
                        self.board[row].append(Piece(row,col,BLACK))
                    else :
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    def get_piece(self,row,col):
        return self.board[row][col]
    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece=self.board[row][col]
                if piece!=0:
                    piece.draw(win)
    def move (self,piece,row,col):
        self.board[piece.row][piece.col],self.board[row][col]=self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)
        if row == ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings+=1
            else:
                self.black_kings+=1
    def get_row_col_from_mouse(self,pos):
        x,y=pos
        row=y//SQUARE_SIZE
        col=x//SQUARE_SIZE
        return row,col
    #def get_valid_moves(self,piece):
            
  
    def get_piece_diag(self,row,col):
        
        sums =row+col
        
        
        board=np.array(self.board)
        diag_left=[]
        diag_right=np.diag(board,col-row )
        diag_right=diag_right.tolist()
        for rows in range(ROWS):
            for cols in range(COLS):
                if (rows +cols == sums):
                    diag_left.append(board[rows,cols])
                    
        
        
        return [diag_right,diag_left]
    def arrange_diag_to_move(self, piece):
        diags = self.get_piece_diag(piece.row, piece.col)
        
        if piece.color == BLACK :
            for i, diag in enumerate(diags):
                diags[i] = diag[::-1]

        for i, diag in enumerate(diags):
            piece_index = diag.index(piece)
            diags[i] = diag[piece_index:]
        
            
        return diags
    def arrange_diag_to_king(self, piece):
        diags = self.get_piece_diag(piece.row,piece.col)
        bol_diag=False
        king_diags=[]
        for i, diag in enumerate(diags):
            piece_index = diag.index(piece)
            if not bol_diag:
                king_diags.extend([diag[:piece_index]])
                bol_diag=True
            if bol_diag:
                king_diags.extend([ diag[piece_index::]])
                bol_diag=False
            diags=king_diags
        for  i,diag in enumerate(diags):
            
            if piece not in diag:
                diags[i].append(piece)
                diags[i]=diag[::-1]
        
        
        return diags
    
        
    def arrange_diag_to_capture(self, piece,k):
        diags = self.get_piece_diag(piece.row, piece.col)
        
        if k==-1 and piece.color == WHITE:
            
            for i, diag in enumerate(diags):
                diags[i] = diag[::-1]

        if  k==0:
            for i, diag in enumerate(diags): 
                diags[i] = diag[::-1]
            
        
        for i, diag in enumerate(diags):
            piece_index = diag.index(piece)
            diags[i] = diag[piece_index:]
        
            
            
        return diags
          
            
            
            
#maybe we use roads
            
    def remove(self,piece):
        row,col=piece.row,piece.col
        self.board[row][col]=0
        if piece.color == BLACK:
            self.black_left-=1
        else:
            self.white_left-=1 
    def no_front_piece(self,piece,valid_moves,i,k):

        if not piece.king:
            valid_moves.append([i])
        else:
            valid_moves.append([k,i//2])
        
    def arrange_ennemy_king_status(self,infront_piece,piece,i,k):
        if piece.king:
            ennemy_diag=self.arrange_diag_to_capture(infront_piece,k)[i//2]
        else:
            ennemy_diag=self.arrange_diag_to_capture(infront_piece,-1)[i]
        return ennemy_diag
    def get_piece_to_capture(self,piece,ennemy_piece,back_piece,i,k,valid_moves):
        if back_piece==0:
            if not piece.king:
                valid_moves.append([i,ennemy_piece])
            else:
                valid_moves.append([k,i//2,ennemy_piece])
        return valid_moves
        
   
                                           
    def extract_possible_moves(self,diags,piece,valid_moves):
        for i,diag in enumerate(diags):
            k=i%2
            ally_iterator=iter(diag)
            
            next(ally_iterator)
            for _ in diag:
                    try:
                        infront_piece = next(ally_iterator)
                        
                    except StopIteration:
                        
                        break
                    
                    if infront_piece ==0  :
                        self.no_front_piece(piece,valid_moves,i,k)
                        break
                        
                        
                            
                    elif infront_piece.color == piece.color:
                        break
                    else:
                        #make this a function in order to handle double jump 
                        
                        ennemy_diag=self.arrange_ennemy_king_status(infront_piece,piece,i,k)#if king i//2 represents left or right and k=i%2 represents up or down 
                        
                        #if not i represents left or right depending on the color 
                        try:
                            ennemy_iterator=iter(ennemy_diag)
                            
                            ennemy_piece=next(ennemy_iterator)
                            back_piece= next(ennemy_iterator)
                            
                            self.get_piece_to_capture(piece,ennemy_piece,back_piece,i,k,valid_moves)
                            
                            
                                
                                
                            break
                                
                        except StopIteration:
                            
                            break   
                                    
                                
                            
                            
                     
    def possible_moves(self,piece):
        valid_moves=[]
        try:
            if piece.king==False:
                diags=self.arrange_diag_to_move(piece)
            else:
                diags=self.arrange_diag_to_king(piece)
        except AttributeError:
            
            return None
        self.extract_possible_moves(diags,piece,valid_moves)
        return valid_moves            
                    
                   
                    
    def choose_valid_piece(self,piece,move):
        if piece.king:
            if len(move)==2:
                piecee=piece
                self.to_capture=False  
            else:
                piecee=move[2]   
                self.to_capture=True  
        else:
                if len(move)==1:
                    piecee=piece
                    self.to_capture=False
                else:
                    piecee=move[1]
                    self.to_capture=True
        return piecee
    def king_movement(self,row,col,move):
        
        if (move[0] ==0):#moving_up
            row=row -1
            if (move[1]==0):#left
                col=col-1
            else: #right
                col=col+1
        else:#buttom
            row=row +1
            if (move[1]==1):#left
                col=col-1
            else: #right
                col=col+1
        return row,col
    def normal_piece_movement(self,row,col,color,move):
        
        if (move[0]==0 and color == BLACK) or (move[0]==1 and color == WHITE): 
            col-=1
            
        else:
            col+=1    
        return row ,col
    def get_valid_moves_position(self,piece):
        moves=self.possible_moves(piece)
        positions={}
        
        
        for move in moves:
            
            piecee=self.choose_valid_piece(piece,move)
            
            col=piecee.col
            if piece.king:
                row=piecee.row
                row,col=self.king_movement(row,col,move)
               
            else:
                row=self.color_row(piecee)
                row,col=self.normal_piece_movement(row,col,piece.color,move)
                   
            if self.to_capture:
                positions[(row,col)]=piecee
            else:
                positions[(row,col)]=None
                        
        return positions
    
        
                
                
                
                   
                    
           
    
                            
                
                    
    def evaluate(self):
        return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
   
    def winner(self):
        if self.black_left <= 0 or  all( not self.get_valid_moves_position(piece) for piece in self.get_all_pieces(BLACK)):
            return WHITE
        elif self.white_left <= 0 or  all( not self.get_valid_moves_position(piece) for piece in self.get_all_pieces(WHITE)):
            return BLACK
        
        return None             
                
    def color_row(self,piece):
        
        if (piece.color == BLACK and self.to_capture==False)or (piece.color==WHITE and self.to_capture == True):
            return piece.row -1
            
        else:
            return piece.row +1      
                 
     
                        
                        
                
                
        
#     def arrange_diag_to_double_jump(self,piece,row,col,k):
#         diags = self.get_piece_diag(row, col)
        
#         for i, diag in enumerate(diags):
#             if i==0 or k==0:
#                 piece_index = min(row,col)
                
#             else:
#                 piece_index = min(row,COLS-col-1)
#             print(f"{piece_index}**************{diag[piece_index]}") 
#             if piece.color == WHITE or k == 0:
#                 diags[i] = diag[:piece_index]
#                 diags[i]=diags[i][::-1]
#             else:
               
#                 diags[i] = diag[piece_index:]
        

        
            
#             #diags[i] = diag[piece_index:]
            
            
            
#         return diags
            
#     def arrange_double_jump_king_status(self,infront_piece,row,col,king,k):
#         if king:
#             ennemy_diags=self.arrange_diag_to_double_jump(infront_piece,row,col,k)
#         else:
#             ennemy_diags=self.arrange_diag_to_double_jump(infront_piece,row,col,-1)
#         return ennemy_diags
#     def get_row_col_double_jump(self,infront_piece,move,piece):
#         if piece.king:
#             row,col=self.king_movement(infront_piece.row,infront_piece.col,move)
#         else:
#             row=self.color_row(infront_piece)
#             row,col=self.normal_piece_movement(row,infront_piece.col,piece.color,move) 
#         return row,col

#  def check_for_double_jump(self,piece1,piece2,color):
#         if piece1 == 0 and piece2 !=0 and piece2.color != color:
#             self.double_jump=True
#         else:
#             self.double_jump=False
#         return self.double_jump
            
            
# if valid_moves:
#                                 move=valid_moves[-1]
#                                 print(f"{move}*************\n")
#                                 row,col=self.get_row_col_double_jump(ennemy_piece,move,piece)
#                                 print(f"{row},,,,,,,,,,,,,,,,,,,,,,,,,,{col}\n")
#                                 double_jump=self.arrange_diag_to_double_jump(ennemy_piece,row,col,k)
#                                 print(double_jump)
                            