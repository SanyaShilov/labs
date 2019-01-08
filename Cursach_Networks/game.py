#!/usr/bin/python3.6

# pylint: disable=invalid-name

EMPTY = 0
BLOCK = 9
WHITE_FIGURES = [1, 2, 3, 4]
BLACK_FIGURES = [5, 6, 7, 8]
TURN_WHITE = SIDE_WHITE = 'white'
TURN_BLACK = SIDE_BLACK = 'black'
LINE_DELTAS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIAGONAL_DELTAS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
ALL_DELTAS = LINE_DELTAS + DIAGONAL_DELTAS
TYPE1 = [1, 5]
TYPE2 = [2, 6]
TYPE3 = [3, 7]
TYPE4 = [4, 8]


class Game:
    def __init__(self, map, white_winning_position,
                 black_winning_position, **kwargs):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)
        self.white_winning_position = white_winning_position
        self.black_winning_position = black_winning_position
        self.turn = TURN_WHITE
        self.selected_cell = None
        self.available_moves = []
        self.locked = False

    def white_win(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] in WHITE_FIGURES:
                    if [i, j] not in self.white_winning_position:
                        return False
        return True

    def black_win(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] in BLACK_FIGURES:
                    if [i, j] not in self.black_winning_position:
                        return False
        return True

    def press_cell(self, i, j):
        if self.locked:
            return {'result': 'NULL'}
        if self.selected_cell:
            if [i, j] in self.available_moves:
                return self._move(i, j)
            return self._deselect()
        if (
                self.map[i][j] in WHITE_FIGURES and self.turn == TURN_WHITE or
                self.map[i][j] in BLACK_FIGURES and self.turn == TURN_BLACK
        ):
            return self._select(i, j)
        return {'result': 'NULL'}

    def _deselect(self):
        self.selected_cell = None
        self.available_moves = []
        return {'result': 'DESELECT'}

    def _move(self, i, j):
        si, sj = self.selected_cell
        self.map[i][j] = self.map[si][sj]
        self.map[si][sj] = EMPTY
        self._deselect()
        self._change_turn()
        return {'result': 'MOVE', 'from': [si, sj], 'to': [i, j]}

    def _select(self, i, j):
        self.available_moves = self._get_available_moves(i, j)
        self.selected_cell = [i, j]
        return {'result': 'SELECT'}

    def _change_turn(self):
        self.turn = TURN_WHITE if self.turn == TURN_BLACK else TURN_BLACK

    @property
    def _friends(self):
        return WHITE_FIGURES if self.turn == TURN_WHITE else BLACK_FIGURES

    def _valid(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    def _get_available_moves(self, i, j):
        if self.map[i][j] in TYPE1:
            return self._get_available_moves1(i, j)
        if self.map[i][j] in TYPE2:
            return self._get_available_moves2(i, j)
        if self.map[i][j] in TYPE3:
            return self._get_available_moves3(i, j)
        if self.map[i][j] in TYPE4:
            return self._get_available_moves4(i, j)
        return []

    def _friends_near(self, i, j):
        result = 0
        for dx, dy in LINE_DELTAS:
            n, m = i + dx, j + dy
            if self._valid(n, m):
                if self.map[n][m] in self._friends:
                    result += 1
        return result

    def _check_direction(self, i, j, dx, dy):
        l = 0
        n, m = i, j
        while True:
            l += 1
            n += dx
            m += dy
            if not self._valid(n, m):
                return 0
            if self.map[n][m] == EMPTY:
                return l
            if self.map[n][m] in self._friends:
                continue
            return 0

    def _get_available_moves1(self, i, j):
        result = []
        for dx, dy in LINE_DELTAS:
            n, m = i + dx, j + dy
            if self._valid(n, m) and self.map[n][m] == EMPTY:
                if self._friends_near(n, m) > 1:
                    result.append([n, m])
        for dx, dy in DIAGONAL_DELTAS:
            n, m = i + dx, j + dy
            if self._valid(n, m) and self.map[n][m] == EMPTY:
                if self._friends_near(n, m) > 0:
                    result.append([n, m])
        return result

    def _get_available_moves3(self, i, j):
        result = []
        for dx, dy in LINE_DELTAS:
            n, m = i + dx, j + dy
            if self._valid(n, m) and self.map[n][m] == EMPTY:
                if self._friends_near(n, m) > 2:
                    result.append([n, m])
        for dx, dy in DIAGONAL_DELTAS:
            n, m = i + dx, j + dy
            if self._valid(n, m) and self.map[n][m] == EMPTY:
                if self._friends_near(n, m) > 1:
                    result.append([n, m])
        return result

    def _get_available_moves2(self, i, j):
        result = []
        for dx, dy in ALL_DELTAS:
            l = self._check_direction(i, j, dx, dy)
            if l > 1:
                result.append([i + dx * l, j + dy * l])
        return result

    def _get_available_moves4(self, i, j):
        result = []
        for dx, dy in ALL_DELTAS:
            l = self._check_direction(i, j, dx, dy)
            if l > 2:
                result.append([i + dx * l, j + dy * l])
        return result
