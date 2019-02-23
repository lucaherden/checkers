from tkinter import *

class CheckersBoard:
    '''represents a board of Checkers'''

    def __init__(self):
        '''CheckersBoard()
        creates a CheckersBoard in starting position'''
        self.board = {}  # dict to store position
        # create opening position
        for row in range(8):
            for column in range(8):
                coords = (row,column)
                if coords in [(0,1),(0,3),(0,5),(0,7),(1,0),(1,2),(1,4),(1,6),(2,1),(2,3),(2,5),(2,7)]:
                    self.board[coords] = 1  # player 1
                elif coords in [(5,0),(5,2),(5,4),(5,6),(6,1),(6,3),(6,5),(6,7),(7,0),(7,2),(7,4),(7,6)]:
                    self.board[coords] = 0  # player 0
                else:
                    self.board[coords] = None  # empty
        self.currentPlayer = 0  # player 0 starts
        self.endgame = None  # replace with string when game ends

    def get_piece(self,coords):
        '''CheckersBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]

    def get_endgame(self):
        '''CheckersBoard.get_endgame() -> None or str
        returns endgame state'''
        return self.endgame

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer

    def next_player(self):
        '''CheckersBoard.next_player()
        advances to next player'''
        self.currentPlayer = 1 - self.currentPlayer

    def get_scores(self):
        '''CheckersBoard.get_scores() -> tuple
        returns a tuple containing player 0's and player 1's scores'''
        pieces = list( self.board.values() )  # list of all the pieces
        # count the number of pieces belonging to both players
        return pieces.count(0), pieces.count(1)
    
    def checkMove(self, coords, newcoords):
        '''CheckersBoard.checkMove -> Boolean
        checks if the move is allowed and if so returns True, otherwise False
        1 - White [Top], 0 - Red [Bottom]'''
        thisPlayer = self.currentPlayer
        otherPlayer = 1 - thisPlayer
        xdiff = newcoords[0] - coords[0]
        #print(xdiff) #[DEBUG]
        ydiff = newcoords[1] - coords[1]
        #print(ydiff) #[DEBUG]
        if (thisPlayer == 0):
            #Possible moveset: +1,+1 or +1,-1
            if ((xdiff == 1) and (ydiff == 1)):
                return True
            elif ((xdiff == 1) and (ydiff == -1)):
                return True
            #Possible moveset: +2,+2 or +2,-2
            elif (xdiff == 2) and (ydiff == 2):
                if (self.board[(coords[0]+1,coords[1]+1)] == 1):
                    self.board[(coords[0]+1,coords[1]+1)] = None
                    return True
            elif (xdiff == 2) and (ydiff == -2):
                if (self.board[(coords[0]+1,coords[1]-1)] == 1):
                    self.board[(coords[0]+1,coords[1]-1)] = None
                    return True
            return False
        elif (thisPlayer == 1):
            #Possible moveset: -1,+1 or -1,-1
            if ((xdiff == -1) and (ydiff == 1)):
                return True
            elif ((xdiff == -1) and (ydiff == -1)):
                return True
            #Possible moveset: -2,+2 or -2,-2
            elif (xdiff == -2) and (ydiff == 2):
                if (self.board[(coords[0]-1,coords[1]+1)] == 0):
                    self.board[(coords[0]-1,coords[1]+1)] = None
                    return True
            elif (xdiff == -2) and (ydiff == -2):
                if (self.board[(coords[0]-1,coords[1]-1)] == 0):
                    self.board[(coords[0]-1,coords[1]-1)] = None
                    return True
            return False

    def try_move(self, coords, oldcoords):
        '''CheckersBoard.try_move(coords, oldcoords)
        places the current player's piece in the square at coords if the square is empty and move is legal
        also removes the old piece at oldcoords and goes to other player's turn'''
        if (self.board[coords] is not None): #if square occupied
            return #do nothing
        #set target square
        self.board[coords] = self.currentPlayer
        #empty original square
        self.board[oldcoords] = None
        self.next_player() #next player
        self.check_endgame() #check if game over

    def check_endgame(self):
        '''CheckersBoard.check_endgame()
        checks if game is over
        updates endgameMessage if over'''
        over = True
        for row in range(8): #check if all squares empty
            for column in range(8):
                coords = (row,column)
                if self.board[coords] is not None:
                    over = False
        if (over):
            scores = self.get_scores()
            if scores[0] > scores[1]:
                self.endgame = 0
            elif scores[0] < scores[1]:
                self.endgame = 1
            else:
                endgame = 'draw'

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c):
        '''CheckersSquare(master,r,c)
        creates a new blank Checkers square at coordinate (r,c)'''
        # create and place the widget
        if ((r+c) % 2 == 0):
            Canvas.__init__(self,master,width=50,height=50,bg='blanched almond')
        else:
            Canvas.__init__(self,master,width=50,height=50,bg='dark green')
        self.grid(row=r,column=c)
        # set the attributes
        self.position = (r,c)
        # bind button click to placing a piece
        self.bind('<Button>',master.get_click)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def make_color(self,color):
        '''CheckersSquare.make_color(color)
        changes color of piece on square to specified color'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10,10,44,44,fill=color)

    def delete_color(self):
        '''CheckersSquare.delete_color()
        removes the piece'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)

class CheckersGame(Frame):
    '''represents a game of Checkers'''

    def __init__(self,master):
        '''CheckersGame(master,[computerPlayer])
        creates a new Checkers game'''
        self.oldCoords = None
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # set up game data
        self.colors = ('red','white')  # players' colors
        # create board in starting position, player 0 going first
        self.board = CheckersBoard() 
        self.squares = {}  # stores CheckersSquares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                self.squares[rc] = CheckersSquare(self,row,column)
        # set up scoreboard and status markers
        self.rowconfigure(8,minsize=3)  # leave a little space
        self.turnSquares = []  # to store the turn indicator squares
        self.scoreLabels = []  # to store the score labels
        # create indicator squares and score labels
        for i in range(2):  
            self.turnSquares.append(CheckersSquare(self,9,7*i))
            self.turnSquares[i].make_color(self.colors[i])
            self.turnSquares[i].unbind('<Button>')
            self.scoreLabels.append(Label(self,text='2',font=('Arial',18) ) )
            self.scoreLabels[i].grid(row=9,column=1+5*i)
        self.passButton = Button(self,text='Pass',command=self.pass_move)
        self.update_display()

    def get_click(self,event):
        '''CheckersGame.get_click(event)
        event handler for mouse click
        gets click data and tries to make the move'''
        coords = event.widget.get_position()
        if (self.oldCoords == None):
            self.oldCoords = coords
            self.squares[coords]['highlightbackground'] = 'blue'
        else:
            if (self.board.checkMove(coords, self.oldCoords)):
                self.board.try_move(coords, self.oldCoords)
                self.squares[self.oldCoords].delete_color() #clear original square
            self.squares[self.oldCoords]['highlightbackground'] = 'white'
            self.oldCoords = None
        # try_move will do the move if valid
        # it will do nothing if not
        self.update_display()  # update the display

    def pass_move(self):
        '''CheckersGame.pass_move()
        event handler for Pass button
        passes for the player's turn'''
        self.board.next_player()  # move onto next player
        self.update_display()

    def update_display(self):
        '''CheckersGame.update_display()
        updates squares to match board
        also updates scoreboard'''
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                piece = self.board.get_piece(rc)
                if piece is not None:
                    self.squares[rc].make_color(self.colors[piece])
                if piece is None:
                    self.squares[rc].delete_color()
        # update the turn indicator
        newPlayer = self.board.get_player()
        oldPlayer = 1 - newPlayer
        self.turnSquares[newPlayer]['highlightbackground'] = 'blue'
        self.turnSquares[oldPlayer]['highlightbackground'] = 'white'
        # update the score displays
        scores = self.board.get_scores()
        for i in range(2):
            self.scoreLabels[i]['text'] = scores[i]
        # if game over, show endgame message
        endgame = self.board.get_endgame()
        if endgame is not None:  # if game is over
            # remove the turn indicator
            self.turnSquares[newPlayer]['highlightbackground'] = 'white'
            if isinstance(endgame,int):  # if a player won
                winner = self.colors[endgame]  # color of winner
                endgameMessage = '{} wins!'.format(winner.title())
            else:
                endgameMessage = "It's a tie!"
            Label(self,text=endgameMessage,font=('Arial',18)).grid(row=9,column=2,columnspan=4)

def play_checkers():
    '''play_checkers()
    starts a new game of Checkers'''
    root = Tk()
    root.title('Checkers')
    CG = CheckersGame(root)
    CG.mainloop()

play_checkers()
