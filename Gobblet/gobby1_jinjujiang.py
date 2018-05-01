
# Tic Tac Toe with AI (Minmax with alpha beta pruning)
# Referred to virtualanup's code
#Modified by Jinju Jiang

import pygame, random, time
from pygame.locals import *
from sys import exit
import math
from collections import defaultdict

# game constants
FPS = 20 #Player levels: beginner 10, middle level 20, expert level 30
starttest = time.time()
players="hr"
timecontrol=180 #time control, eg, if 180 seconds elapsed and there was no action, then game over

# color codes
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 200)
red = (200, 0, 0)
green = (0, 200, 0)

cross = 1
circle = 2
empty = 0

computer = 1
human = 2


class Player:
    #'''base class for the players'''

    def __init__(self, type, sign, name):
        '''Initializer for player class.

        Keyword Arguments:
        type -- Type of the player (computer or humann)
        sign -- sign assigned to the player (cross or circle)
        name -- name of the player '''
        self.type = type
        self.sign = sign
        self.name = name

    def SetBoard(self, board):
        '''sets the board on which the player is playing'''
        self.board = board

    def GetMove(self):
        pass

    # process click of mouse
    def MouseClick(self, cell):
        pass

    def OppositeSign(self, sign):
        '''returns the sign of the opponent'''
        if sign == circle:
            return cross
        return circle


# the human player class. handles mouse clicks
class HumanPlayer(Player):
    '''Human player class. '''

    def __init__(self, sign, name):
        super().__init__(human, sign, name)  # human player
        self.lastmove = -1

    def GetMove(self):
        '''Returns the next move. in case of human, it waits
        until a mouse click is detected in the board.'''
        if (self.lastmove != -1):
            move = self.lastmove
            self.lastmove = -1
            print(self.name,"moves to:",move)
            return move

    def MouseClick(self, cell):
        '''Records the cell to which the human player checked

        Keyword arguments:
        cell : The cell in which mouse was clicked'''

        if not cell in self.board.moves:  # it no move in the position
            self.lastmove = cell
            starttest = time.time()



class ComputerPlayer(Player):
    '''Computer player class. '''

    def __init__(self, sign, name):
        super().__init__(computer, sign, name)  # computer player
        self.lastmove = -1

    def GetMove(self):
        '''Returns the next move. Computer player uses minmax algorithm
        to determine the next move'''
        # just a minor optimization : if it is the first move, always place in the center
        #if len(possiblemoves) == 9:
          #  return (1, 1)
        self.maxdepth = 100
        self.loop = 0
        val, move = self.MaxValue(-9, 9)
        print(self.loop," moves")
        print (self.name,"moves to:",move)
        return move

    def GetScore(self):
        '''Utility function for determining the numerical value of terminal condition.
        Called in game over condition'''
        if self.board.Draw():
            return 0
        elif self.board.GetWinner() == self.sign:
            return 1
        return -1  # the other player won

    def MaxValue(self, alpha, beta):
        '''maxvalue returns the maximized score and position for the player's move'''
        maxpos = None
        maxval = -9

        for move in self.board.getFreePositions():
            self.loop += 1
            self.board.Move(move, self.sign)

            if self.board.GameOver():
                newval = self.GetScore()
            else:
                newval, movepos = self.MinValue(alpha, beta)

            self.board.UndoMove()

            if newval > beta:
                return newval, move
            if newval > alpha:
                alpha = newval

            if newval > maxval:
                maxval = newval
                maxpos = move
            if newval == 1:
                break;

        return maxval, maxpos

    def MinValue(self, alpha, beta):
        '''minvalue returns the minimized score and position for the opponent's move'''
        minpos = None
        minval = 9

        for move in self.board.getFreePositions():
            self.loop += 1
            self.board.Move(move, self.OppositeSign(self.sign))

            if self.board.GameOver():
                newval = self.GetScore()
            else:
                newval, movepos = self.MaxValue(alpha, beta)

            self.board.UndoMove()

            if newval < alpha:
                return newval, move
            if newval < beta:
                beta = newval

            if newval < minval:
                minval = newval
                minpos = move
            if newval == -1:
                break;

        return minval, minpos


class BoardAnalyzer:
    '''Boardanalyzer class is used as an interface to the board'''

    possiblecells = [(a, b) for a in range(0, 3) for b in range(0, 3)]
    alllines = [[(a, b) for a in range(0, 3)] for b in range(0, 3)] + [[(b, a) for a in range(0, 3)] for b in
                                                                       range(0, 3)] + [[(0, 0), (1, 1), (2, 2)],
                                                                                       [(0, 2), (1, 1), (2, 0)]]

    def __init__(self):
        self.moves = []  # this will store the moves.
        self.gameover = False
        self.draw = False
        self.board = defaultdict(lambda: empty)  # board is a dictionary that is initially empty

    def getFreePositions(self):
        '''Each player can place his move in any free position'''
        return [x for x in self.possiblecells if not x in self.moves]

    def Move(self, position, symbol):
        '''move to the given position.
        Keyword Arguments:

        position -- position to place the move
        symbol -- the symbol to place in the position'''
        # if the board position is free,copy an item to it
        if self.board[position] != empty:
            return False
        self.board[position] = symbol
        self.moves.append(position)
        self.CheckGameOver()
        return True

    def UndoMove(self):
        '''Undo the previous move.'''
        if len(self.moves) == 0:
            return False
        self.board[self.moves.pop()] = empty
        # There can be no more moves after game over. So, ser gameover to false just in case
        # the last move resulted in game over.
        self.gameover = False
        return True

    def GameOver(self):
        return self.gameover

    def Draw(self):
        return self.draw

    def GetWinner(self):
        '''returns the winner of the game'''
        if self.GameOver() and not self.Draw():
            return self.winner

    def CheckGameOver(self):
        '''checks the game over condition'''
        for line in self.alllines:
            px, py, pz = line
            if self.board[px] != empty and self.board[px] == self.board[py] == self.board[pz]:
                self.gameover = True
                self.winner = self.board[px]
                self.draw = False
                break
        else:
            if len(self.moves) == 9:
                self.draw = True
                self.gameover = True
            else:
                self.gameover = False


class Board:
    '''the actual board'''
    gridcolor = blue
    circlecolor = red
    crosscolor = green

    def __init__(self, boardsize=400):
        self.players = []
        self.boardsize = boardsize
        self.gameboard = BoardAnalyzer()
        self.font = pygame.font.Font(None, 30)  # load the font for displaying text

    def reset(self):
        '''resets the game board'''
        self.gameboard = BoardAnalyzer()
        # notify the players about the new game board
        for player in self.players:
            player.SetBoard(self.gameboard)
        # whoever loses gets the first chance
        self.player1, self.player2 = self.player2, self.player1
        starttest = time.time()


    def printstatus(self, screen):
        textstr = ''
        if game.gameboard.GameOver():
            if game.gameboard.Draw():
                textstr = "Draw. Click here to reset"
            else:
                textstr = self.player1.name + " wins. Click here to reset"
        else:
            textstr = self.player1.name + "'s turn" +" Time:"+str(int(time.time()-starttest))
        text = self.font.render(textstr, 1, (255, 255, 255))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=self.boardsize + 5)
        screen.blit(text, textpos)

    def AddPlayer(self, player):
        player.SetBoard(self.gameboard)
        self.players.append(player)
        if (len(self.players) > 1):
            self.player1 = self.players[0]
            self.player2 = self.players[1]

    def draw(self, screen):
        # draw the board in blue color
        tolerance = 20
        pygame.draw.line(screen, self.gridcolor, (self.boardsize / 3, tolerance),
                         (self.boardsize / 3, self.boardsize - tolerance), 10)
        pygame.draw.line(screen, self.gridcolor, ((2 * self.boardsize) / 3, tolerance),
                         ((2 * self.boardsize) / 3, self.boardsize - tolerance), 10)
        pygame.draw.line(screen, self.gridcolor, (tolerance, (self.boardsize) / 3),
                         (self.boardsize - tolerance, (self.boardsize) / 3), 10)
        pygame.draw.line(screen, self.gridcolor, (tolerance, (2 * self.boardsize) / 3),
                         (self.boardsize - tolerance, (2 * self.boardsize) / 3), 10)

        # draw each cross or circle
        for move in self.gameboard.moves:
            mx, my = move
            onethird = int(self.boardsize / 3)

            if self.gameboard.board[move] == circle:
                # draw a circle in that position
                pos = mx * onethird + int(onethird / 2), my * onethird + int(onethird / 2)
                pygame.draw.circle(screen, self.circlecolor, pos, int(onethird / 3), 0)
                starttest = time.time()
            elif self.gameboard.board[move] == cross:
                pos = mx * onethird + int(onethird / 2), my * onethird + int(onethird / 2)
                pygame.draw.circle(screen, self.crosscolor, pos, int(onethird / 3), 0)
                starttest = time.time()
        # get items from board analyzer and draw the required items

    def MouseClick(self, position):
        # get the cell position and pass it to the player(s)
        mx, my = position
        if my < self.boardsize:  # if inside range
            onethird = int(self.boardsize / 3)
            cx = int(math.floor(mx / onethird))
            cy = int(math.floor(my / onethird))
            cell = cx, cy
            self.player1.MouseClick(cell)  # pass along to the player
        elif self.gameboard.GameOver():
            self.reset()

    def update(self):
        # update the board
        if not self.gameboard.GameOver():
            nextpos = self.player1.GetMove()
            if nextpos is not None:
                # move the player in that position
                self.gameboard.Move(nextpos, self.player1.sign)
                # if any player caused game over, keep him as player 1
                if not self.gameboard.GameOver():
                    self.player1, self.player2 = self.player2, self.player1  # exchange the players
                    starttest = time.time()
if (__name__ == "__main__"):
    pygame.init()
    boardsize = 400
    screen = pygame.display.set_mode((boardsize, boardsize + 35))
    pygame.display.set_caption('Tic Tac Toe')
    gameover = False
    clock = pygame.time.Clock()
    game = Board()
    if players == "hr" or players == "rh":
        game.AddPlayer(ComputerPlayer(cross, "Robot"))
        game.AddPlayer(HumanPlayer(circle, "Human"))
    elif players == "h2":
        game.AddPlayer(HumanPlayer(circle, "Human1"))
        game.AddPlayer(HumanPlayer(cross, "Human2"))
    if players == "r2":
        game.AddPlayer(ComputerPlayer(circle, "Robot1"))
        game.AddPlayer(ComputerPlayer(cross, "Robot2"))



    while gameover == False:
        clock.tick(FPS)
        screen.fill(black);
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit();
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                game.MouseClick(event.pos)
                starttest = time.time()
        game.update()
        game.draw(screen)
        game.printstatus(screen)
        pygame.display.update()
        if (time.time() - starttest) > timecontrol:
            gameover = True
            print("game over because of time elapsed")
