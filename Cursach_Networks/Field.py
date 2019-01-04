class Field:
    def winningPosition(self):
        return self._winningPosition
    
    def __init__ (self, width, height,
                  blocks = [], ones = [], twoes = [], threes = [], fours = [],
                  winpos = []):
        self.width = width
        self.height = height
        self.matrix = [[-1 for j in range(width)] for i in range(height)]
        for i, j in blocks :
            self.matrix[i][j] = 0
        for i, j in ones :
            self.matrix[i][j] = 1
        for i, j in twoes :
            self.matrix[i][j] = 2
        for i, j in threes :
            self.matrix[i][j] = 3
        for i, j in fours :
            self.matrix[i][j] = 4
        self._winningPosition = winpos.copy()
        self._getAvailableMoves()
        self._movestack = []
        self._selectedCell = None

    def index(self, i, j):
        return self.matrix[i][j]

    def set(self, i, j, val):
        self.matrix[i][j] = val

    def isValid(self, i, j):
        return (i >= 0) & (i < self.width) & (j >= 0) & (j < self.height)

    def isBlock(self, i, j):
        return not self.matrix[i][j]

    def isEmpty(self, i, j):
        return self.matrix[i][j] < 0

    def isFigure(self, i, j):
        return self.matrix[i][j] > 0
        
    @classmethod
    def load(cls, filename):
        f = open(filename)
        r = f.readlines()
        f.close()
        width, height = [int(k) for k in r[0].split()]
        blocks = []
        ones = []
        twoes = []
        threes = []
        fours = []
        for i in range(2, height+2):
            for j in range(width) :
                if r[i][j] == '0' :
                    blocks.append((i - 2, j))
                elif r[i][j] == '1' :
                    ones.append((i - 2, j))
                elif r[i][j] == '2' :
                    twoes.append((i - 2, j))
                elif r[i][j] == '3' :
                    threes.append((i - 2, j))
                elif r[i][j] == '4' :
                    fours.append((i - 2, j))
        winpos = []
        for i in range(3+height, len(r)):
            winpos.append(tuple(int(k) for k in r[i].split()))
        field = cls(width, height, blocks, ones, twoes, threes, fours, winpos) 
        return field

    def availableMoves(self):
        return self._availableMoves

    def selectedCell(self):
        return self._selectedCell

    def pressCell(self, i, j):
        if self._selectedCell :
            self._move(i, j)
        else :
            if self.isFigure(i, j) :
                self._selectedCell = (i, j)

    def _move(self, i, j):
        si, sj = self._selectedCell
        if (i, j) in self._availableMoves[si][sj] :
            self.matrix[i][j] = self.matrix[si][sj]
            self.matrix[si][sj] = -1
            self._movestack.append((si, sj, i, j))
            if len(self._movestack) > 100 :
                self._movestack.pop(0)
            self._getAvailableMoves()
        self._selectedCell = None

    def undo(self):
        if self._movestack :
            i, j, newi, newj = self._movestack.pop()
            self.matrix[i][j] = self.matrix[newi][newj]
            self.matrix[newi][newj] = -1
            self._getAvailableMoves()

    def _getLineNeighbours(self, i, j):
        neighbours = []
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            if self.isValid(i+dx, j+dy):
                neighbours.append((i+dx, j+dy))
        return neighbours

    def _getDiagonalNeighbours(self, i, j):
        neighbours = []
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            if self.isValid(i+dx, j+dy):
                neighbours.append((i+dx, j+dy))
        return neighbours

    def _figuresInLineNeighbours(self, i, j):
        ln = self._getLineNeighbours(i, j)
        f = 0
        for n, m in ln:
            if self.isFigure(n, m):
                f += 1
        return f

    def _getAvailableMoves(self):
        self._availableMoves = [[[] for j in range(self.width)]
                                for i in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] == 1 :
                    self._getAvailableMove1(i, j)
                elif self.matrix[i][j] == 2:
                    self._getAvailableMove2(i, j)
                elif self.matrix[i][j] == 3:
                    self._getAvailableMove3(i, j)
                elif self.matrix[i][j] == 4:
                    self._getAvailableMove4(i, j)

    def _checkDirection(self, i, j, dx, dy):
        l = 0
        n, m = i, j
        while True:
            l += 1
            n += dx
            m += dy
            if not self.isValid(n, m):
                return 0
            if self.isEmpty(n, m):
                return l
            if self.isBlock(n, m):
                return 0

    def _getAvailableMove1(self, i, j):
        ln = self._getLineNeighbours(i, j)
        for n, m in ln:
            if self.isEmpty(n, m):
                if self._figuresInLineNeighbours(n, m) > 1:
                    self._availableMoves[i][j].append((n, m))
        dn = self._getDiagonalNeighbours(i, j)
        for n, m in dn:
            if self.isEmpty(n, m):
                if self._figuresInLineNeighbours(n, m) > 0:
                    self._availableMoves[i][j].append((n, m))

    def _getAvailableMove2(self, i, j):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx or dy:
                    l = self._checkDirection(i, j, dx, dy)
                    if l > 1:
                        self._availableMoves[i][j].append((i+dx*l, j+dy*l))

    def _getAvailableMove3(self, i, j):
        ln = self._getLineNeighbours(i, j)
        for n, m in ln:
            if self.isEmpty(n, m):
                if self._figuresInLineNeighbours(n, m) > 2:
                    self._availableMoves[i][j].append((n, m))
        dn = self._getDiagonalNeighbours(i, j)
        for n, m in dn:
            if self.isEmpty(n, m):
                if self._figuresInLineNeighbours(n, m) > 1:
                    self._availableMoves[i][j].append((n, m))

    def _getAvailableMove4(self, i, j):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx or dy:
                    l = self._checkDirection(i, j, dx, dy)
                    if l > 2:
                        self._availableMoves[i][j].append((i+dx*l, j+dy*l))
