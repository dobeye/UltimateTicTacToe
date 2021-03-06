import pygame

LINE_COLOR = (0, 85, 75)
SIZE = 1000
BORDER = 5


class Board:
    RECURSION_LEVEL = 2
    ZERO_POP = False
    WASTED_TURNS = False
    PlayArea = []

    def __init__(self, screen, position=4, place=((0, 0), (SIZE, SIZE)), level=0, parent=None):
        self.winner = 0
        self.board_array = [[0 for _ in range(3)] for _ in range(3)]
        self.screen = screen

        self.level = level
        self.parent = parent
        self.position = position
        self.length = place[1][0] - place[0][0]
        self.playable = level == Board.RECURSION_LEVEL

        self.place = place
        length = place[1][0] - place[0][0]
        self.width = max(1, 10 - level * 4)
        if self.parent is not None:
            dif = self.parent.line / 2 + self.width
        else:
            dif = BORDER

        # region draw board
        pygame.draw.line(screen, LINE_COLOR,
                         (place[0][0] + length / 3, place[0][1] + dif),
                         (place[0][0] + length / 3, place[1][1] - dif),
                         self.width)
        pygame.draw.line(screen, LINE_COLOR,
                         (place[0][0] + length * 2 / 3, place[0][1] + dif),
                         (place[0][0] + length * 2 / 3, place[1][1] - dif),
                         self.width)
        pygame.draw.line(screen, LINE_COLOR,
                         (place[0][0] + dif, place[0][1] + length / 3),
                         (place[1][0] - dif, place[0][1] + length / 3),
                         self.width)
        pygame.draw.line(screen, LINE_COLOR,
                         (place[0][0] + dif, place[0][1] + length * 2 / 3),
                         (place[1][0] - dif, place[0][1] + length * 2 / 3),
                         self.width)
        # endregion

        # create inner boards for every position in the current board
        self.inner_boards = []
        if not self.playable:
            for i in range(9):
                self.inner_boards.append(Board(screen, i, ((place[0][0] + (place[1][0] - place[0][0]) * (i % 3) / 3,
                                                            place[0][1] + (place[1][1] - place[0][1]) * (i // 3) / 3),
                                                           (place[0][0] + (place[1][0] - place[0][0]) * (i % 3 + 1) / 3,
                                                            place[0][1] + (place[1][1] - place[0][1]) * (
                                                                    i // 3 + 1) / 3)),
                                               (level + 1), self))

    def play(self, position, player):
        position = int(position)
        self.board_array[position // 3][position % 3] = player

        # draw X/Circle depending on the player, and if the player is neither 1 nor 2, raise an error
        if player == 1:
            pygame.draw.line(self.screen, LINE_COLOR,
                             (self.place[0][0] + self.length * (position % 3) / 3,
                              self.place[0][1] + self.length * (position // 3) / 3),
                             (self.place[0][0] + self.length * ((position % 3) + 1) / 3,
                              self.place[0][1] + self.length * ((position // 3) + 1) / 3), self.width)
            pygame.draw.line(self.screen, LINE_COLOR,
                             (self.place[0][0] + self.length * ((position % 3) + 1) / 3,
                              self.place[0][1] + self.length * (position // 3) / 3),
                             (self.place[0][0] + self.length * (position % 3) / 3,
                              self.place[0][1] + self.length * ((position // 3) + 1) / 3), self.width)
        elif player == -1:
            pygame.draw.circle(self.screen, LINE_COLOR,
                               (self.place[0][0] + self.length * ((position % 3) * 2 + 1) / 6,
                                self.place[0][1] + self.length * ((position // 3) * 2 + 1) / 6),
                               self.length / 6, self.width)
        else:
            raise Exception("InvalidPlayer")

        # set up play area for the next player depending on selected rules
        if Board.ZERO_POP:
            if self.playable:
                Board.PlayArea.pop(0)
        elif self.parent is not None:
            Board.PlayArea = Board.PlayArea[:self.level]
            Board.PlayArea[-1] = position
        elif Board.RECURSION_LEVEL == 0:
            Board.PlayArea = []
        print(Board.PlayArea)

        # check winner
        for i in range(3):
            if abs(sum(self.board_array[i])) == 3:
                self.winner = self.board_array[i][0]
            elif abs(sum([self.board_array[j][i] for j in range(3)])) == 3:
                self.winner = self.board_array[0][i]
            else:
                continue
            break
        if abs(sum(self.board_array[i][2 - i] for i in range(3))) == 3 or \
                abs(sum(self.board_array[i][i] for i in range(3))) == 3:
            self.winner = self.board_array[1][1]

        if self.winner != 0:
            if self.parent is not None:
                if self.parent.availability(self.position):
                    self.parent.play(self.position, self.winner)
            else:
                # this will only happen when a player has won the game,
                # so everything that happens when someone wins (confetti and all) goes here
                print(f"player {int(self.winner == -1) + 1} wins")

    def availability(self, position):
        return self.board_array[int(position / 3)][position % 3] == 0

    @property
    def tie(self):
        return all(all(x != 0 for x in y) for y in self.board_array)

    def get_board(self, position):
        if self.level < Board.RECURSION_LEVEL:
            return self.inner_boards[position]
        else:
            raise RecursionError

    @property
    def open(self):
        return any(any(x == 0 for x in y) for y in self.board_array) and (Board.WASTED_TURNS or self.winner == 0)

    @property
    def border(self):
        return self.place

    @property
    def size(self):
        return self.length

    @property
    def line(self):
        return self.width
