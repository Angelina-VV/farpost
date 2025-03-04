from typing import List

def tic_tac_toe_checker(board: List[List[str]]) -> str:
    # Function to check for a winner
    def check_winner(player: str) -> bool:
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if all(cell == player for cell in board[i]):  # Check rows
                return True
            if all(board[j][i] == player for j in range(3)):  # Check columns
                return True
        # Check diagonals
        if all(board[i][i] == player for i in range(3)):  # Check main diagonal
            return True
        if all(board[i][2 - i] == player for i in range(3)):  # Check anti-diagonal
            return True
        return False
    
    x_wins = check_winner('x')
    o_wins = check_winner('o')

    if x_wins:
        return "x wins!"
    if o_wins:
        return "o wins!"
    
    # Check for unfinished game and draw scenario
    if any(cell == '-' for row in board for cell in row):
        return "unfinished!"
    else:
        return "draw!"

# Example usage
if __name__ == "__main__":
    board1 = [['-', '-', 'o'],
               ['-', 'x', 'o'],
               ['x', 'o', 'x']]
    print(tic_tac_toe_checker(board1))  # Output: "unfinished!"

    board2 = [['-', '-', 'o'],
               ['-', 'o', 'o'],
               ['x', 'x', 'x']]
    print(tic_tac_toe_checker(board2))  # Output: "x wins!"