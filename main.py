import pygame
import sys
import Board
from Board import SIZE, Board

BG_COLOR = (28, 170, 156)
WHITE = (255, 255, 255)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Ultimate Tic Tac Toe")
    screen.fill(BG_COLOR)
    board = None
    available_board = None

    turn = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                # pressing anywhere on an empty board
                if turn == 0:
                    board = Board(screen, 4)
                    turn += 1
                # pressing in the available board
                elif available_board.border[0][0] < mouse_x < available_board.border[1][0] and \
                        available_board.border[0][1] < mouse_y < available_board.border[1][1]:

                    # Identify the played board
                    played_board = board
                    temp = []
                    while True:
                        pos = int((mouse_x - played_board.border[0][0]) // (played_board.size / 3) +
                                  3 * ((mouse_y - played_board.border[0][1]) // (played_board.size / 3)))
                        temp.append(pos)
                        if not played_board.playable:
                            played_board = played_board.get_board(pos)
                        else:
                            break

                    if played_board.availability(pos) and played_board.open:
                        Board.PlayArea = temp
                        played_board.play(pos, -(-1) ** turn)
                        turn += 1

                available_board = board
                for x in Board.PlayArea:
                    if available_board.get_board(x).open or \
                            (Board.WASTED_TURNS and not available_board.get_board(x).tie):
                        available_board = available_board.get_board(x)
                    else:
                        break

        pygame.display.update()


if __name__ == "__main__":
    main()
