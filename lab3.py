from typing import List

def tic_tac_toe_checker(board: List[List[str]]) -> str:
    # Для проверки победителя
    def check_winner(player: str) -> bool:
        # Проверка строк, столбцов и диагоналей на победу
        for i in range(3):
            if all(cell == player for cell in board[i]):  
                return True
            if all(board[j][i] == player for j in range(3)):  
                return True
        
        if all(board[i][i] == player for i in range(3)):  
            return True
        if all(board[i][2 - i] == player for i in range(3)): 
            return True
        return False
    
    x_wins = check_winner('x')
    o_wins = check_winner('o')

    if x_wins:
        return "x wins!"
    if o_wins:
        return "o wins!"
    
    # Проверка на незаконченную игру и ничью
    if any(cell == '-' for row in board for cell in row):
        return "unfinished!"
    else:
        return "draw!"

if __name__ == "__main__":
    board1 = [['-', '-', 'o'],
               ['-', 'x', 'o'],
               ['x', 'o', 'x']]
    print(tic_tac_toe_checker(board1))  # Output: "unfinished!"

    board2 = [['-', '-', 'o'],
               ['-', 'o', 'o'],
               ['x', 'x', 'x']]
    print(tic_tac_toe_checker(board2))  # Output: "x wins!"