from pygame import mixer
import time
import sys
import pygame
n = 8


# RGB CODES FOR COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)


# DIMENSIONS FOR CHESS BOARD
WIDTH, HEIGHT = 480, 480
ROWS, COLUMNS = 8, 8
one_square = WIDTH//COLUMNS  # Size of each square in the chessboard
IMAGES = {}

FPS = 5


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Knights Tour')  # caption for the game


def LoadImages():
    pieces = ['bN', 'target', 'knightW', 'knightW2']
    for piece in pieces:
        im = pygame.image.load(str(piece)+".png")
        IMAGES[piece] = pygame.transform.scale(im, (one_square, one_square))


gd = pygame.display.set_mode((480, 480))    # Starting screen with play button


def GameIntro():
    pygame.init()
    background_image = pygame.image.load("background3.png")
    intro = False
    while intro == False:
        gd.blit(background_image, (0, 0))
        Buttons(100, 300, "PLAY")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = True
        pygame.display.update()


def Message(size, mess, x_pos, y_pos):  # Displays the message "PLAY" on that button that we created
    font = pygame.font.SysFont(None, size)
    render = font.render(mess, True, WHITE)
    gd.blit(render, (x_pos, y_pos))


def Buttons(x_button, y_button, mess_b):  # CREATES "PLAY" BUTTON ON THE SCREEN
    pygame.draw.rect(gd, GREEN, [x_button, y_button, 100, 30])
    Message(50, mess_b, x_button, y_button)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x_button < mouse[0] < x_button+100 and y_button < mouse[1] < y_button+30:
        pygame.draw.rect(gd, LIGHT_GREEN, [x_button, y_button, 100, 30])
        Message(50, mess_b, x_button, y_button)
        if click == (1, 0, 0) and mess_b == "PLAY":
            main()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def display():  # DISPLAYS THE MESSAGE THAT SOLUTION DOES NOT EXIST, IF THATS THE CASE
    font = pygame.font.SysFont(None, 36)
    render = font.render('SOLUTION DOES NOT EXIST!', True, RED)
    WIN.blit(render, (100, 300))


def inside_board(x1, y1, board):  # TO CHECK IF WE'RE STILL INSIDE THE BOARD AND THE MOVES EXIST

    if(x1 >= 0 and y1 >= 0 and x1 < n and y1 < n and board[x1][y1] == -1):
        return True
    return False


def final(n, board):  # RETURNS US A LIST WHICH HAS ALL THE NUMBERS ASSIGNED THAT WHERE KNIGHT HAS TO MOVE EACH TIME
    lst = []
    for i in range(n):
        lst_ = []
        for j in range(n):
            lst_.append(board[i][j])
        lst.append(lst_)
    return(lst)


def knight_tour(n):

    # INITIALIZING THE BOARD
    lst = []
    for i in range(n):
        lst_ = []
        for j in range(n):
            lst_.append(-1)
        lst.append(lst_)
    board = lst

    # THESE ARE THE MOVES A KNIGHT CAN MAKE, SINCE IT MOVES IN L-DIRECTION ON THE BOARD
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    board[0][0] = 0
    count = 1

    if(not solve_func(n, board, 0, 0, move_x, move_y, count)):
        return("NO SOLUTION FOUND")
    else:
        return(final(n, board))


# RECURSIVE FUNCTION THAT FINDS THE POSSIBLE MOVES
def solve_func(n, board, current_x, current_y, move_x, move_y, count):

    if(count == n**2):
        return True

    for i in range(8):
        new_x = current_x + move_x[i]
        new_y = current_y + move_y[i]
        if(inside_board(new_x, new_y, board)):
            board[new_x][new_y] = count
            if(solve_func(n, board, new_x, new_y, move_x, move_y, count+1)):
                return True

            # Backtracking
            board[new_x][new_y] = -1
    return False


class Board():  # FIRST THREE FUNCTIONS HELP IN DRAWING THE 8x8 CHESSBOARD
    def __init__(self):
        self.board = [["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"]]
        # YOU CAN DECIDE THE INITIAL POSITION FOR KNIGHT AND PLACE IT BELOW:
        self.board[0][0] = "bN"
        self.selected_piece = None

    def draw_cubes(self, win):
        win.fill(GRAY)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row*one_square,
                                 col*one_square, one_square, one_square))

    def draw_pieces(self, win):
        for row in range(ROWS):
            for col in range(ROWS):
                piece = self.board[row][col]
                if piece != "-":
                    win.blit(IMAGES[piece], pygame.Rect(
                        row*one_square, col*one_square, one_square, one_square))

    # DISPLAYS THE POSITIONS WHERE KNIGHT HAS TO MOVE ONE BY ONE
    def knightmovement(self, win):

        # EXTRACTING THE LIST OF NUMBERS FROM OUR KNIGHT TOUR FUNC
        res = knight_tour(8)
        clock = pygame.time.Clock()
        fps = 3
        if type(res) == str:  # solution doesn't exist in this case, so that message will display on the screen
            display()
        else:  # FORMING A LIST OF TUPLES SO THAT WE CAN PLACE OUR KNIGHT EASILY
            lst = []
            for i in range(0, 64):
                for j in res:
                    for k in j:
                        if k == i:
                            ind = j.index(k)
                            ind2 = res.index(j)
                lst.append((ind2, ind))
            moves_ = lst
            for i in moves_:
                x = int(i[0])
                y = int(i[1])
                index = moves_.index(i)
                piece = self.board[x][y]
                if piece == "bN":
                    pass
                elif piece == "-":
                    # Places all the Knights on screen one by one
                    win.blit(IMAGES["knightW"], (x*one_square, y*one_square))
                    clock.tick(fps)
                    pygame.display.update()


def main():  # MAIN FUNCTION THAT CALLS THE REST OF OUR FUNCTIONS
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    board = Board()
    LoadImages()
    board.draw_cubes(WIN)
    board.draw_pieces(WIN)
    mixer.music.load('background.wav')  # ADDS MUSIC AND LOOPS ON IT
    mixer.music.play(-1)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass

        pygame.display.update()
        clock.tick(FPS)
        board.knightmovement(WIN)
        pygame.display.update()

    pygame.quit()


GameIntro()
main()
