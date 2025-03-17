"""Основной модуль для запуска игры.
Содержит функцию main, которая управляет игровым процессом.
"""

from board import Board


def main():
    """
    Основная функция для запуска игры.

    Запрашивает у пользователя выбор типа игры, настраивает доску и управляет игровым процессом.
    """
    print("Выберите тип игры:")
    print("1. Шахматы")
    print("2. Модифицированные шахматы")
    print("3. Шашки")
    
    
    game_type_mapping = {
        "1": "chess",
        "2": "modified_chess",
        "3": "checkers"
    }
    
    
    while True:
        choice = input("Введите номер (1-3): ").strip()
        if choice in game_type_mapping:
            game_type = game_type_mapping[choice]
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите номер от 1 до 3.")
    
    
    board = Board(game_type)
    board.setup_board()
    board.display()
    
    current_player = "white"
    
    
    while True:
        print(f"\nТекущее количество ходов: {board.move_count}")
        move = input(f"Ход {current_player.capitalize()} (например, 'E2 E4', 'undo' для отмены или 'quit' для выхода): ")
        
        if move.lower() == "quit":
            print("Игра завершена.")
            print("\nИстория ходов:")
            if not board.move_history:
                print("Ходов не было.")
            else:
                for i, move in enumerate(board.move_history, 1):
                    print(f"{i}. {move.current_player.capitalize()}: {move.from_pos} -> {move.to_pos}")
            break
        
        if move.lower() == "undo":
            new_player = board.undo_move()
            if new_player is not None:
                current_player = new_player
            continue
        
        if move.lower() == "hint":
            board.display_with_threats(current_player)
            continue
        
        try:
            from_pos, to_pos = move.split()
            figure = board.get_figure(from_pos)
            if figure is None:
                print("На начальной позиции нет фигуры.")
                continue
            
            if figure.color != current_player:
                print("Вы можете двигать только свои фигуры.")
                continue
            
            board.move_figure(from_pos, to_pos, current_player)
            current_player = "black" if current_player == "white" else "white"
            board.display_with_threats(current_player)
        
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()