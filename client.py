import connect4

print("select name for the human player:")
name = input()
connect4 = connect4.Connect4Game(player1=name)
connect4.start_game()
print("game start")

# todo invalid input
while(not connect4.is_game_over()):
    if connect4.is_current_player_computer():
        print("computer places a checker")
        ls = connect4.place_token()
        for _ in ls:
            print(_)
        print("\n")
    else:
        print(connect4.get_current_player(), "please select a column to place checker:")
        col = int(input())
        ls = connect4.place_token(col)
        for _ in ls:
            print(_)
        print("\n")
winner = connect4.get_winner()
print("winner is: ", winner)
