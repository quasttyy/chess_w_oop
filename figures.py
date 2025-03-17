"""
Модуль для работы с фигурами.
Содержит классы всех фигур и их логику перемещения.
"""

class Figure:
    """
    Базовый класс для всех фигур.

    Attributes:
        color (str): Цвет фигуры.
        row (int): Номер строки на доске.
        column (int): Номер столбца на доске.
        symbol (str): Символ фигуры.
    """

    def __init__(self, color):
        """
        Инициализирует объект Figure.

        Args:
            color (str): Цвет фигуры.
        """
        self.color = color
        self.row = None
        self.column = None
        self.symbol = None

    def set_position(self, row, column):
        """
        Устанавливает позицию фигуры на доске.

        Args:
            row (int): Номер строки.
            column (int): Номер столбца.
        """
        self.row = row
        self.column = column

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли фигура переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.

        Raises:
            NotImplementedError: Если метод не переопределен в подклассе.
        """
        raise NotImplementedError("Этот метод должен быть реализован в подклассах")


class Pawn(Figure):
    """Класс для пешки."""

    def __init__(self, color):
        """
        Инициализирует объект Pawn.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "P" if color == "white" else "p"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли пешка переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        direction = -1 if self.color == "white" else 1
        start_row = 6 if self.color == "white" else 1

        if to_column == self.column and to_row == self.row + direction:
            if board.board[to_row][to_column] == ".":
                return True

        if (to_column == self.column and to_row == self.row + 2 * direction and
                self.row == start_row and board.board[to_row][to_column] == "." and
                board.board[self.row + direction][self.column] == "."):
            return True

        if (abs(to_column - self.column) == 1 and to_row == self.row + direction):
            if board.board[to_row][to_column] != "." and board.figures[(to_row, to_column)].color != self.color:
                return True
            elif not board.get_piece(to_row, to_column):
                last_move = board.last_move
                if last_move:
                    last_from, last_to, last_piece = last_move
                    if (last_piece.__class__ == Pawn and
                        abs(last_to[0] - last_from[0]) == 2 and
                        last_to[0] == self.row and last_to[1] == to_column):
                        return True

        return False


class Rook(Figure):
    """Класс для ладьи."""

    def __init__(self, color):
        """
        Инициализирует объект Rook.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "R" if color == "white" else "r"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли ладья переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        if to_row == self.row and to_column != self.column:
            step = 1 if to_column > self.column else -1
            for col in range(self.column + step, to_column, step):
                if board.board[self.row][col] != ".":
                    return False
            return True
        if to_column == self.column and to_row != self.row:
            step = 1 if to_row > self.row else -1
            for row in range(self.row + step, to_row, step):
                if board.board[row][self.column] != ".":
                    return False
            return True
        return False


class Knight(Figure):
    """Класс для коня."""

    def __init__(self, color):
        """
        Инициализирует объект Knight.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "N" if color == "white" else "n"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли конь переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        row_diff = abs(to_row - self.row)
        col_diff = abs(to_column - self.column)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)


class Bishop(Figure):
    """Класс для слона."""

    def __init__(self, color):
        """
        Инициализирует объект Bishop.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "B" if color == "white" else "b"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли слон переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        if abs(to_row - self.row) == abs(to_column - self.column):
            row_step = 1 if to_row > self.row else -1
            col_step = 1 if to_column > self.column else -1
            row, col = self.row + row_step, self.column + col_step
            while row != to_row and col != to_column:
                if board.board[row][col] != ".":
                    return False
                row += row_step
                col += col_step
            return True
        return False


class Queen(Figure):
    """Класс для ферзя."""

    def __init__(self, color):
        """
        Инициализирует объект Queen.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "Q" if color == "white" else "q"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли ферзь переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        rook = Rook(self.color)
        bishop = Bishop(self.color)
        rook.set_position(self.row, self.column)
        bishop.set_position(self.row, self.column)
        return (rook.can_move(to_row, to_column, board) or
                bishop.can_move(to_row, to_column, board))


class King(Figure):
    """Класс для короля."""

    def __init__(self, color):
        """
        Инициализирует объект King.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "K" if color == "white" else "k"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли король переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        row_diff = abs(to_row - self.row)
        col_diff = abs(to_column - self.column)
        return max(row_diff, col_diff) == 1


class Checker(Figure):
    """Класс для шашки."""

    def __init__(self, color):
        """
        Инициализирует объект Checker.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "C" if color == "white" else "c"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли шашка переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        direction = -1 if self.color == "white" else 1
        row_diff = to_row - self.row
        col_diff = abs(to_column - self.column)

        if row_diff == direction and col_diff == 1:
            if board.board[to_row][to_column] == ".":
                return True

        if row_diff == 2 * direction and col_diff == 2:
            mid_row = self.row + direction
            mid_col = (self.column + to_column) // 2
            if (board.board[mid_row][mid_col] != "." and 
                board.figures[(mid_row, mid_col)].color != self.color and 
                board.board[to_row][to_column] == "."):
                return True

        return False


class CheckerKing(Figure):
    """Класс для дамки в шашках."""

    def __init__(self, color):
        """
        Инициализирует объект CheckerKing.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "K" if color == "white" else "k"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли дамка переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        if abs(to_row - self.row) != abs(to_column - self.column):
            return False

        row_step = 1 if to_row > self.row else -1
        col_step = 1 if to_column > self.column else -1
        row, col = self.row + row_step, self.column + col_step
        enemy_found = False
        enemy_pos = None

        while row != to_row and col != to_column:
            if board.board[row][col] != ".":
                if board.figures[(row, col)].color == self.color:
                    return False
                elif enemy_found:
                    return False
                else:
                    enemy_found = True
                    enemy_pos = (row, col)
            row += row_step
            col += col_step

        if board.board[to_row][to_column] != ".":
            return False

        if enemy_found:
            board.enemy_to_capture = enemy_pos
        else:
            board.enemy_to_capture = None

        return True


class LightRook(Figure):
    """Класс для легкой ладьи в модифицированных шахматах."""

    def __init__(self, color):
        """
        Инициализирует объект LightRook.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "L" if color == "white" else "l"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли легкая ладья переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        row_diff = to_row - self.row
        col_diff = to_column - self.column

        # Движение по горизонтали на 1 или 2 клетки
        if row_diff == 0 and abs(col_diff) in [1, 2]:
            step = 1 if col_diff > 0 else -1
            for col in range(self.column + step, to_column, step):
                if board.board[self.row][col] != ".":
                    return False
            return True
        # Движение по вертикали на 1 или 2 клетки
        elif col_diff == 0 and abs(row_diff) in [1, 2]:
            step = 1 if row_diff > 0 else -1
            for row in range(self.row + step, to_row, step):
                if board.board[row][self.column] != ".":
                    return False
            return True
        return False


class ShortBishop(Figure):
    """Класс для короткого слона в модифицированных шахматах."""

    def __init__(self, color):
        """
        Инициализирует объект ShortBishop.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "S" if color == "white" else "s"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли короткий слон переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        row_diff = abs(to_row - self.row)
        col_diff = abs(to_column - self.column)

        if row_diff == col_diff and row_diff in [1, 2]:
            row_step = 1 if to_row > self.row else -1
            col_step = 1 if to_column > self.column else -1
            row, col = self.row + row_step, self.column + col_step
            while row != to_row and col != to_column:
                if board.board[row][col] != ".":
                    return False
                row += row_step
                col += col_step
            return True
        return False


class Guardian(Figure):
    """Класс для стража в модифицированных шахматах."""

    def __init__(self, color):
        """
        Инициализирует объект Guardian.

        Args:
            color (str): Цвет фигуры.
        """
        super().__init__(color)
        self.symbol = "G" if color == "white" else "g"

    def can_move(self, to_row, to_column, board):
        """
        Проверяет, может ли страж переместиться на указанную позицию.

        Args:
            to_row (int): Номер строки назначения.
            to_column (int): Номер столбца назначения.
            board (Board): Объект доски.

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        row_diff = abs(to_row - self.row)
        col_diff = abs(to_column - self.column)
        return max(row_diff, col_diff) == 1