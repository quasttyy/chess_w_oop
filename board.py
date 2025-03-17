"""
Модуль для работы с шахматной доской и управления игровым процессом.
"""

from figures import Pawn, Rook, Knight, Bishop, Queen, King as ChessKing, Checker, CheckerKing, LightRook, ShortBishop, Guardian
import copy


class MoveHistory:
    """
    Класс для хранения информации о выполненном ходе.

    Attributes:
        from_pos (str): Позиция, с которой была перемещена фигура.
        to_pos (str): Позиция, на которую была перемещена фигура.
        moved_figure (Figure): Фигура, которая была перемещена.
        captured_figure (Figure): Фигура, которая была взята (если есть).
        last_move (tuple): Информация о последнем ходе.
        board_state (tuple): Состояние доски и фигур перед ходом.
        current_player (str): Игрок, который выполнил ход.
    """

    def __init__(self, from_pos, to_pos, moved_figure, captured_figure, last_move, board_state, current_player):
        """
        Инициализирует объект MoveHistory.

        Args:
            from_pos (str): Позиция, с которой была перемещена фигура.
            to_pos (str): Позиция, на которую была перемещена фигура.
            moved_figure (Figure): Фигура, которая была перемещена.
            captured_figure (Figure): Фигура, которая была взята (если есть).
            last_move (tuple): Информация о последнем ходе.
            board_state (tuple): Состояние доски и фигур перед ходом.
            current_player (str): Игрок, который выполнил ход.
        """
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.moved_figure = moved_figure
        self.captured_figure = captured_figure
        self.last_move = last_move
        self.board_state = board_state
        self.current_player = current_player


class Board:
    """
    Класс для управления шахматной доской и игровым процессом.

    Attributes:
        game_type (str): Тип игры (шахматы, шашки, модифицированные шахматы).
        board (list): Двумерный список, представляющий доску.
        figures (dict): Словарь, хранящий фигуры и их позиции.
        last_move (tuple): Информация о последнем выполненном ходе.
        move_history (list): История всех ходов.
        enemy_to_capture (tuple): Позиция фигуры, которую нужно взять (для шашек).
        move_count (int): Счетчик количества выполненных ходов.
    """

    def __init__(self, game_type="chess"):
        """
        Инициализирует объект Board.

        Args:
            game_type (str, optional): Тип игры. По умолчанию "chess".
        """
        self.game_type = game_type
        self.board = self.create_board()
        self.figures = {}
        self.last_move = None
        self.move_history = []
        self.enemy_to_capture = None
        self.move_count = 0

    def create_board(self):
        """
        Создает пустую шахматную доску.

        Returns:
            list: Двумерный список, представляющий пустую доску.
        """
        return [["." for _ in range(8)] for _ in range(8)]

    def display(self, threatened_positions=None):
        """
        Отображает текущее состояние доски.

        Args:
            threatened_positions (set, optional): Множество позиций, находящихся под угрозой.
        """
        if threatened_positions is None:
            threatened_positions = set()

        print("  A B C D E F G H")
        for i, row in enumerate(self.board):
            print(f"{8 - i} ", end="")
            for j, cell in enumerate(row):
                if cell != ".":
                    pos = (i, j)
                    if pos in threatened_positions:
                        # Красный цвет для угрожаемых фигур
                        print(f"\033[91m{cell}\033[0m", end=" ")
                    else:
                        print(cell, end=" ")
                else:
                    print(cell, end=" ")
            print(f"{8 - i}")
        print("  A B C D E F G H")

    def algebraic_to_indices(self, position):
        """
        Преобразует алгебраическую нотацию в индексы доски.

        Args:
            position (str): Позиция в алгебраической нотации (например, "A1").

        Returns:
            tuple: Кортеж (строка, столбец).

        Raises:
            ValueError: Если позиция некорректна.
        """
        if len(position) != 2 or not position[0].isalpha() or not position[1].isdigit():
            raise ValueError("Некорректная позиция.")
        column = ord(position[0].lower()) - ord('a')
        row = 8 - int(position[1])
        return row, column

    def indices_to_algebraic(self, row, column):
        """
        Преобразует индексы доски в алгебраическую нотацию.

        Args:
            row (int): Номер строки.
            column (int): Номер столбца.

        Returns:
            str: Позиция в алгебраической нотации.
        """
        column_letter = chr(column + ord('a'))
        row_number = 8 - row
        return str(column_letter.upper()) + str(row_number)

    def place_figure(self, figure, position):
        """
        Размещает фигуру на доске.

        Args:
            figure (Figure): Фигура для размещения.
            position (str): Позиция на доске.

        Raises:
            ValueError: Если клетка уже занята.
        """
        row, column = self.algebraic_to_indices(position)
        if self.board[row][column] != ".":
            raise ValueError("Данная клетка уже занята. Попробуйте снова.")
        self.board[row][column] = figure.symbol
        self.figures[(row, column)] = figure
        figure.set_position(row, column)

    def remove_figure(self, position):
        """
        Удаляет фигуру с доски.

        Args:
            position (str): Позиция фигуры.

        Raises:
            ValueError: Если на клетке нет фигуры.
        """
        row, column = self.algebraic_to_indices(position)
        if self.board[row][column] == ".":
            raise ValueError(f"На клетке {position} нет фигуры для удаления.")
        self.board[row][column] = "."
        del self.figures[(row, column)]

    def get_piece(self, row, column):
        """
        Возвращает фигуру по индексам.

        Args:
            row (int): Номер строки.
            column (int): Номер столбца.

        Returns:
            Figure: Фигура или None, если клетка пуста.
        """
        return self.figures.get((row, column), None)

    def get_figure(self, position):
        """
        Возвращает фигуру по позиции.

        Args:
            position (str): Позиция в алгебраической нотации.

        Returns:
            Figure: Фигура или None, если клетка пуста.
        """
        row, column = self.algebraic_to_indices(position)
        return self.get_piece(row, column)

    def save_state(self):
        """
        Сохраняет текущее состояние доски и фигур.

        Returns:
            tuple: Кортеж (состояние доски, состояние фигур).
        """
        board_copy = copy.deepcopy(self.board)
        figures_copy = copy.deepcopy(self.figures)
        return board_copy, figures_copy

    def restore_state(self, board_state, figures_state, last_move):
        """
        Восстанавливает состояние доски и фигур.

        Args:
            board_state (list): Состояние доски.
            figures_state (dict): Состояние фигур.
            last_move (tuple): Информация о последнем ходе.
        """
        self.board = board_state
        self.figures = figures_state
        self.last_move = last_move

    def setup_board(self):
        """Настраивает доску в зависимости от типа игры."""
        if self.game_type == "chess":
            self.setup_chess()
        elif self.game_type == "checkers":
            self.setup_checkers()
        elif self.game_type == "modified_chess":
            self.setup_modified_chess()

    def setup_chess(self):
        """Настраивает доску для игры в шахматы."""
        self.place_figure(Rook("white"), "A1")
        self.place_figure(Knight("white"), "B1")
        self.place_figure(Bishop("white"), "C1")
        self.place_figure(Queen("white"), "D1")
        self.place_figure(ChessKing("white"), "E1")
        self.place_figure(Bishop("white"), "F1")
        self.place_figure(Knight("white"), "G1")
        self.place_figure(Rook("white"), "H1")
        for column in "ABCDEFGH":
            self.place_figure(Pawn("white"), column + "2")

        self.place_figure(Rook("black"), "A8")
        self.place_figure(Knight("black"), "B8")
        self.place_figure(Bishop("black"), "C8")
        self.place_figure(Queen("black"), "D8")
        self.place_figure(ChessKing("black"), "E8")
        self.place_figure(Bishop("black"), "F8")
        self.place_figure(Knight("black"), "G8")
        self.place_figure(Rook("black"), "H8")
        for column in "ABCDEFGH":
            self.place_figure(Pawn("black"), column + "7")

    def setup_checkers(self):
        """Настраивает доску для игры в шашки."""
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pos = self.indices_to_algebraic(row, col)
                    self.place_figure(Checker("white"), pos)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pos = self.indices_to_algebraic(row, col)
                    self.place_figure(Checker("black"), pos)

    def setup_modified_chess(self):
        """Настраивает доску для игры в модифицированные шахматы."""
        self.place_figure(LightRook("white"), "A1")
        self.place_figure(Guardian("white"), "B1")
        self.place_figure(ShortBishop("white"), "C1")
        self.place_figure(Queen("white"), "D1")
        self.place_figure(ChessKing("white"), "E1")
        self.place_figure(ShortBishop("white"), "F1")
        self.place_figure(Guardian("white"), "G1")
        self.place_figure(LightRook("white"), "H1")
        for column in "ABCDEFGH":
            self.place_figure(Pawn("white"), column + "2")

        self.place_figure(LightRook("black"), "A8")
        self.place_figure(Guardian("black"), "B8")
        self.place_figure(ShortBishop("black"), "C8")
        self.place_figure(Queen("black"), "D8")
        self.place_figure(ChessKing("black"), "E8")
        self.place_figure(ShortBishop("black"), "F8")
        self.place_figure(Guardian("black"), "G8")
        self.place_figure(LightRook("black"), "H8")
        for column in "ABCDEFGH":
            self.place_figure(Pawn("black"), column + "7")

    def is_guardian_protected(self, row, column, color):
        """
        Проверяет, защищен ли Guardian союзной фигурой.

        Args:
            row (int): Номер строки.
            column (int): Номер столбца.
            color (str): Цвет фигуры.

        Returns:
            bool: True, если Guardian защищен, иначе False.
        """
        for r in range(max(0, row - 1), min(8, row + 2)):
            for c in range(max(0, column - 1), min(8, column + 2)):
                if r == row and c == column:
                    continue
                piece = self.get_piece(r, c)
                if piece and piece.color == color:
                    return True
        return False

    def move_figure(self, from_position, to_position, current_player):
        """
        Перемещает фигуру на доске.

        Args:
            from_position (str): Позиция, с которой перемещается фигура.
            to_position (str): Позиция, на которую перемещается фигура.
            current_player (str): Текущий игрок.

        Raises:
            ValueError: Если ход невозможен.
        """
        from_row, from_column = self.algebraic_to_indices(from_position)
        to_row, to_column = self.algebraic_to_indices(to_position)

        if self.board[from_row][from_column] == ".":
            raise ValueError("Данная клетка пуста. Выберите фигуру, для того чтобы походить.")

        figure = self.figures[(from_row, from_column)]

        if figure.color != current_player:
            raise ValueError("Вы можете двигать только свои фигуры.")

        if not figure.can_move(to_row, to_column, self):
            raise ValueError(f"Фигура на {from_position} не может походить на {to_position}.")

        # Проверка на взятие Guardian
        if self.board[to_row][to_column] != ".":
            target_figure = self.figures[(to_row, to_column)]
            if (target_figure.__class__ == Guardian and 
                self.is_guardian_protected(to_row, to_column, target_figure.color)):
                raise ValueError("Нельзя взять Guardian, пока он защищён союзной фигурой.")

        board_state, figures_state = self.save_state()
        captured_figure = self.get_piece(to_row, to_column)

        # Взятие на проходе для шахмат
        if self.game_type == "chess" and figure.__class__ == Pawn and abs(to_column - from_column) == 1 and self.board[to_row][to_column] == ".":
            if self.last_move:
                last_from, last_to, last_piece = self.last_move
                if (last_piece.__class__ == Pawn and
                    abs(last_to[0] - last_from[0]) == 2 and
                    last_to[0] == from_row and last_to[1] == to_column):
                    captured_figure = self.get_piece(last_to[0], last_to[1])
                    self.board[last_to[0]][last_to[1]] = "."
                    del self.figures[(last_to[0], last_to[1])]

        # Логика для шашек
        if self.game_type == "checkers":
            if figure.__class__ == Checker and abs(to_row - from_row) == 2:
                mid_row = (from_row + to_row) // 2
                mid_col = (from_column + to_column) // 2
                captured_figure = self.get_piece(mid_row, mid_col)
                self.board[mid_row][mid_col] = "."
                del self.figures[(mid_row, mid_col)]
            elif figure.__class__ == CheckerKing and self.enemy_to_capture:
                enemy_row, enemy_col = self.enemy_to_capture
                captured_figure = self.get_piece(enemy_row, enemy_col)
                self.board[enemy_row][enemy_col] = "."
                del self.figures[(enemy_row, enemy_col)]
                self.enemy_to_capture = None

        if self.board[to_row][to_column] != ".":
            if self.figures[(to_row, to_column)].color == figure.color:
                raise ValueError(f"Нельзя походить на {to_position}, там стоит ваша фигура.")
            else:
                self.remove_figure(to_position)

        self.board[from_row][from_column] = "."
        del self.figures[(from_row, from_column)]
        self.figures[(to_row, to_column)] = figure
        figure.set_position(to_row, to_column)
        self.board[to_row][to_column] = figure.symbol

        self.last_move = ((from_row, from_column), (to_row, to_column), figure)
        self.move_history.append(MoveHistory(
            from_position, to_position, figure, captured_figure, self.last_move, (board_state, figures_state), current_player
        ))

        # Увеличиваем счетчик ходов
        self.move_count += 1

        # Превращение пешки в шахматах
        if self.game_type == "chess" and figure.__class__ == Pawn:
            if (figure.color == "white" and to_row == 0) or (figure.color == "black" and to_row == 7):
                self.promote_pawn(to_row, to_column, figure.color)

        # Превращение шашки в дамку
        if self.game_type == "checkers" and figure.__class__ == Checker:
            if (figure.color == "white" and to_row == 0) or (figure.color == "black" and to_row == 7):
                new_king = CheckerKing(figure.color)
                new_king.set_position(to_row, to_column)
                self.figures[(to_row, to_column)] = new_king
                self.board[to_row][to_column] = new_king.symbol

        # Превращение LightRook в обычную ладью в модифицированных шахматах
        if self.game_type == "modified_chess" and figure.__class__ == LightRook:
            if (figure.color == "white" and to_row == 0) or (figure.color == "black" and to_row == 7):
                new_rook = Rook(figure.color)
                new_rook.set_position(to_row, to_column)
                self.figures[(to_row, to_column)] = new_rook
                self.board[to_row][to_column] = new_rook.symbol

    def promote_pawn(self, row, column, color):
        """
        Превращает пешку в другую фигуру.

        Args:
            row (int): Номер строки.
            column (int): Номер столбца.
            color (str): Цвет фигуры.
        """
        choice = input("Выберите фигуру для замены (Q - ферзь, R - ладья, B - слон, N - конь): ").upper()
        while choice not in ["Q", "R", "B", "N"]:
            choice = input("Некорректный выбор. Введите Q, R, B или N: ").upper()

        if choice == "Q":
            new_figure = Queen(color)
        elif choice == "R":
            new_figure = Rook(color)
        elif choice == "B":
            new_figure = Bishop(color)
        elif choice == "N":
            new_figure = Knight(color)

        self.board[row][column] = new_figure.symbol
        self.figures[(row, column)] = new_figure
        new_figure.set_position(row, column)

    def undo_move(self):
        """Отменяет последний ход.

        Returns:
            str: Игрок, который должен сделать следующий ход.
        """
        if not self.move_history:
            print("Нет ходов для отмены.")
            return None

        last_move = self.move_history.pop()
        board_state, figures_state = last_move.board_state
        self.restore_state(board_state, figures_state, last_move.last_move)
        self.last_move = last_move.last_move

        self.move_count -= 1

        print(f"Откат хода: {last_move.from_pos} -> {last_move.to_pos}")
        self.display()
        return last_move.current_player

    def get_player_figures(self, color):
        """
        Возвращает все фигуры указанного цвета.

        Args:
            color (str): Цвет фигур.

        Returns:
            list: Список фигур.
        """
        return [figure for figure in self.figures.values() if figure.color == color]

    def is_position_under_threat(self, row, column, opponent_color):
        """
        Проверяет, находится ли позиция под угрозой.

        Args:
            row (int): Номер строки.
            column (int): Номер столбца.
            opponent_color (str): Цвет соперника.

        Returns:
            bool: True, если позиция под угрозой, иначе False.
        """
        for figure in self.figures.values():
            if figure.color == opponent_color:
                if figure.can_move(row, column, self):
                    return True
        return False

    def get_threatened_figures(self, current_player):
        """
        Возвращает список угрожаемых фигур и флаг шаха.

        Args:
            current_player (str): Текущий игрок.

        Returns:
            tuple: Список угрожаемых позиций и флаг шаха.
        """
        opponent_color = "black" if current_player == "white" else "white"
        threatened = []
        king_under_check = False
        for pos, figure in self.figures.items():
            if figure.color == current_player:
                if self.is_position_under_threat(pos[0], pos[1], opponent_color):
                    threatened.append(pos)
                    if figure.__class__ == ChessKing:
                        king_under_check = True
        return threatened, king_under_check

    def display_with_threats(self, current_player):
        """
        Отображает доску с выделением угрожаемых фигур.

        Args:
            current_player (str): Текущий игрок.
        """
        threatened_positions, king_under_check = self.get_threatened_figures(current_player)
        self.display(set(threatened_positions))
        if king_under_check:
            print("Король под шахом!")
        if threatened_positions:
            print("Угрожаемые фигуры:", [self.indices_to_algebraic(*pos) for pos in threatened_positions])
        else:
            print("Нет угрожаемых фигур.")