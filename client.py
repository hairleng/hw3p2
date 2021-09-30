import connect4
# Client implementation of the human to computer connect4 game

# utility method to print the board


def print_board(board):
    board.reverse()
    for _ in board:
        print(_)
    print("\n")


# variable to keep the loop
isGameEnd = False

while (not isGameEnd):
    print("select name for the human player:")
    # listen to user input
    name = input()
    try:
        # initialize connect 4 game with one human player and one computer player
        connect4 = connect4.Connect4Game(player1=name)
        # start the game
        connect4.start_game()
        print("game start")

        while(not connect4.is_game_over()):
            if connect4.is_current_player_computer():
                print("Computer places a checker")
                board = connect4.place_token()
                # print board
                print_board(board)
            else:
                print(connect4.get_current_player(),
                      "please select a column to place checker:")
                s = input()
                while not s.isnumeric() or int(s) < 0 or int(s) > 6:
                    print("Please enter a valid number(0~6):")
                    s = input()
                col = int(s)
                # check if the placement is valid then place the checker
                if connect4.is_placement_valid(col):
                    # place a move
                    board = connect4.place_token(col)
                    # prepare board to be printed
                    print_board(board)
                else:
                    # print error message for invalid column
                    print("Invalid Column!!\n")

        winner = connect4.get_winner()
        print("winner is: ", winner)
        # exit the loop and end the game
        isGameEnd = True
    # handling value error exception
    except ValueError as ve:
        print(ve)
