  def make_mini_board(self , piece ):
        if piece==0:
            return None
        row=piece.row
        col=piece.col
        if row != 0 and row != 7 and col != 0 and col != 7:
            mini_board_matrix=np.zeros((3,3),dtype=Piece)
            mini_board_matrix[0,0]=self.board[row-1][col-1]
            mini_board_matrix[0,2]=self.board[row-1][col+1]
            mini_board_matrix[1,1]=self.board[row][col]
            mini_board_matrix[2,0]=self.board[row+1][col-1]
            mini_board_matrix[2,2]=self.board[row+1][col+1]
            
            
    
        elif row==0 and col !=7:
            mini_board_matrix=np.zeros((2,3),dtype=Piece)
            mini_board_matrix[0,1]=self.board[row][col]
            mini_board_matrix[1,0]=self.board[row+1][col-1]
            mini_board_matrix[1,2]=self.board[row+1][col+1]
            
        elif row==7 and  col!=0:
            mini_board_matrix=np.zeros((2,3),dtype=Piece)
            mini_board_matrix[0,0]=self.board[row-1][col-1]
            mini_board_matrix[0,2]=self.board[row-1][col+1]
            mini_board_matrix[1,1]=self.board[row][col]
        elif  row ==7 and col==0 :
            mini_board_matrix=np.zeros((2,2),dtype=Piece)
            mini_board_matrix[1,0]=self.board[row][col]
            mini_board_matrix[0,1]=self.board[row-1][col+1]
        elif  row==0  and col ==7:
            mini_board_matrix=np.zeros((2,2),dtype=Piece)
            mini_board_matrix[0,1]=self.board[row][col]
            mini_board_matrix[1,0]=self.board[row+1][col-1]
        elif  col == 0 and row<7 and row>0:
            mini_board_matrix=np.zeros((3,2),dtype=Piece)
            mini_board_matrix[0,1]=self.board[row-1][col+1]
            mini_board_matrix[1,0]=self.board[row][col]
            mini_board_matrix[2,1]=self.board[row+1][col+1]
        elif col ==7 and row<7 and row>0:
            mini_board_matrix=np.zeros((3,2),dtype=Piece)
            mini_board_matrix[0,0]=self.board[row-1][col-1]
            mini_board_matrix[1,1]=self.board[row][col]
            mini_board_matrix[2,0]=self.board[row+1][col-1]
        return mini_board_matrix
        
    def capture(self,piece,ennemy_piece,move):
            self.move(piece,move[0],move[1])
            self.remove(ennemy_piece)
        
    #def draw_valid_moves(self,piece,moves):
         
    
            
    def check_surrounded_pieces(self,piece):
        if piece:
            mini_board=self.make_mini_board(piece)
        else:
            return None
        surrounded_pieces=[]
        behind_piece=[]
        infront_piece=[]
        for pieces in mini_board:
            for piecee in pieces:
                if piecee !=0 and piecee !=piece:
                    
                    
                        if piecee.row==piece.row+1:
                            if piece.color == WHITE:
                                infront_piece.append(piecee)
                            else:
                                behind_piece.append(piecee)
                        else:
                            if piece.color == BLACK:
                                infront_piece.append(piecee)
                            else:
                                behind_piece.append(piecee)
            
                    
                
                    
                         
                    
        if behind_piece or infront_piece:
            mini_board=np.array(mini_board,dtype=Piece)
            if len(behind_piece)==0 and (np.shape(mini_board)==(2,2) or np.shape(mini_board)==(2,3)):
                surrounded_pieces.append(infront_piece)
                return surrounded_pieces
            surrounded_pieces.append(behind_piece)
            surrounded_pieces.append(infront_piece)      
                 
        return surrounded_pieces
    def check_right_with_piece(self,piece,other_piece):
        if piece.col<other_piece.col:
            return True
        else:
            return False
    def check_right_with_pos(self,piece,pos):
        if piece.col<pos[1]:
            return True
        else:
            return False   
    def     get_moving_to_row(self,piece):
        row=piece.row
        
        if piece.color ==BLACK:
            row-=1
        else:
            row+=1
        return row
    def get_pos_of_valid_moves(self, piece):
        
        if piece:
            surrounded=self.check_surrounded_pieces(piece) 
            
        else:
            return None
        
        valid_moves=[]
        
        if self.on_edge(piece) == False:
            infront_pieces=surrounded[1]
        
            valid_move=self.generate_valid_moves(piece,infront_pieces)
            valid_moves,path=valid_move
            return valid_moves,path
        
            
                

                            
        return valid_moves                    
                    
            
        
                                    
            
                    
    def remove(self,piece):
        row,col=piece.row,piece.col
        self.board[row][col]=0
        if piece.color == BLACK:
            self.black_left-=1
        else:
            self.white_left-=1
                  
                       
    def check_empty_on_diagonal_after_infront_piece(self,piece,back,right):
        if len(back)==0:
            return True
        elif len(back)==2:
            return False
        else:
            if right:
                col=back[1].col +1
            else:
                col=back[0].col -1
                
            if self.check_right_with_pos(back,(self.get_moving_to_row(piece),col)):
                return False
            else:
                return True
            
                    
    def generate_valid_moves(self, piece, infront_pieces):
        col=piece.col
        row_direction=self.get_moving_to_row(piece)

        valid_moves = []
        pieces_according_to_move = []
        length=len(infront_pieces)
        
        if len(infront_pieces)==0:
            valid_moves.extend([ (row_direction,col+1),(row_direction,col-1)])
                
        else:
            if length == 1:
                right = self.check_right_with_pos(piece,(infront_pieces[0].row,infront_pieces[0].col))
                coll=self.inv_right_col(col,right)
                valid_moves.append((row_direction, coll))
                
                    
                    
            for infront_piece in infront_pieces:
                right = self.check_right_with_piece(piece, infront_piece)
                if self.on_edge(infront_piece) :
                    
                    continue
            
                
                
                    
                else:
                    surrounded_pieces = self.check_surrounded_pieces(infront_piece)
                    surrounded_piece = surrounded_pieces[0]
                    if self.check_empty_on_diagonal_after_infront_piece(piece,surrounded_piece, right):
                        
                        infront_col=self.right_col(infront_piece.col,right)
                        infront_row=self.color_row(infront_piece.row,piece.color)
                        valid_moves.append( (infront_row,infront_col ))
                        
                    
                    pieces_according_to_move.append(infront_piece)        
               
                    
                
                            
                        
            
        return valid_moves,pieces_according_to_move
    
    
    
    def on_edge(self, piece):
        if piece.row==7 or piece.row==0 or piece.col==7 or piece.col==0:
            return True 
        else:
            return False         
    def right_col(self,col,right):
        if right:
            return col +1
        else:
            return col -1  
    def inv_right_col(self,col,right):
        if right:
            return col -1
        else:
            return col +1                
    def color_row(self,row,color):
        if color == BLACK:
            return row -1
        else:
            return row+1