import pygame
import sys
import time
from pygame import mixer
global N

##################### YOU CAN CHANGE THE VALUE OF N BELOW: ##########################
N = 10
#####################################################################################


# RGB CODES FOR COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)


# DIMENSIONS FOR CHESS BOARD
WIDTH, HEIGHT = 480, 480
ROWS, COLUMNS = N, N
one_square = WIDTH//COLUMNS  # Size of each square in the chessboard
IMAGES = {}

FPS = 1


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('N-Queens')  # Caption for the game


def LoadImages():
    pieces = ['queen', 'queenW']
    for piece in pieces:
        im = pygame.image.load(str(piece)+".png")
        IMAGES[piece] = pygame.transform.scale(im, (one_square, one_square))


gd = pygame.display.set_mode((480, 480))  # Starting screen with play button


def GameIntro():
    pygame.init()
    background_image = pygame.image.load("background2.png")
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


def final(board):
    for i in range(N):
        for j in range(N):
            x = 2
    return(board)


def inside_boardd(board, row, col):

    # Check on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check lower diagonal and upper diagonal on left side
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def solve_funcc(board, col):
    # ALL QUEENS HAVE BEEN PLACED, BASE CASE
    if col >= N:
        return True

    for i in range(N):

        if inside_boardd(board, i, col):
            board[i][col] = 1

            # RECURSION FOR THEE REST OF QUEENS
            if solve_funcc(board, col + 1) == True:
                return True

            # DOESNT LEAD TO A SOLUTION SO WE REMOVE IT FROM HERE
            board[i][col] = 0

    return False


def NQ_problem(N):
    # AN NxN CHESS BOARD
    lst = []
    for i in range(N):
        lst_ = []
        for j in range(N):
            lst_.append(0)
        lst.append(lst_)
    board = lst
    if solve_funcc(board, 0) == False:
        return False

    # A list of lists, in which all the numbers in the first list represent the nth time they'll appear
    return(final(board))
    # and the index of that number means it will appear on that block of chessboard.
    # To suit our problem, we'll create tuples from this list later on that help us in allocating the place
    # for queen to appear.


class Board():
    def __init__(self):  # FIRST THREE FUNCTIONS HELP IN DRAWING THE NxN CHESSBOARD
        lst = []
        for i in range(N):
            lst_ = []
            for j in range(N):
                lst_.append("-")
            lst.append(lst_)
        self.board = lst
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

    # DISPLAYS THE POSITIONS WHERE QUEENS HAVE TO BE PLACED
    def queenmovement(self, win):
        board = NQ_problem(N)
        clock = pygame.time.Clock()
        fps = 2.5
        if board == False:  # solution doesn't exist in this case, so that message will display on the screen
            display()
        else:  # otherwise, proceed with making tuples from the list that we got from NQ_problem function
            p = 0
            main_lst = []
            while p < len(board):
                move = board[p]
                for number in move:
                    if number == 1:
                        ind = move.index(number)
                    else:
                        pass
                main_lst.append((p, ind))
                p = p+1
            res = main_lst
            for i in (res):
                x = int(i[0])
                y = int(i[1])
                index = res.index(i)
                piece = self.board[x][y]
                if piece == "-":  # Places the Queens one by one
                    win.blit(IMAGES["queenW"], (x*one_square, y*one_square))
                    clock.tick(fps)
                    pygame.display.update()


def main():  # MAIN FUNCTION THAT CALLS ALL THE OTHER FUNCTIONS
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    board = Board()
    LoadImages()
    board.draw_cubes(WIN)
    board.draw_pieces(WIN)
    # Plays music as the game start, on a loop
    mixer.music.load('background.wav')
    mixer.music.play(-1)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When you click on the RED cross button on the top of screen, it exists the game
                pygame.quit()
                sys.exit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass

        pygame.display.update()
        board.queenmovement(WIN)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


GameIntro()
main()
