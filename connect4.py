"""
@author Gram Liu (gdl2)
@author Marci McBride (marcim)
Connect4 API
"""
from typing import Dict, Optional, List
import random
import copy

class Connect4Game:
  """Initializes a game of Connect 4.

    Initializes a game of Connect4 with the given player names passed in as arguments.
    If no player names are passed in, the game will initialize with two computer
    players. If one player name is passed in, the game will be initialized with one
    computer player and one human player. If two player names are passed in, the game
    will initialize with the two human players.

    Args:
      player1: The name of the first player, or "Computer1" if not specified.
      player2: The name of the second player, or "Computer2" if not specified.

    Returns:
      A new Connect4Game instance.

    Raises:
      ValueError: If the names of the two players are the same or if the passed 
                  names are either "Computer1" or "Computer2"
    """
  def __init__(self, player1: Optional[str] = None, player2: Optional[str] = None):
    reserved_names = ["Computer1", "Computer2"]
    if player1 in reserved_names:
      raise ValueError("Attempted to use reserved name! Cannot use: " + player1)
    if player2 in reserved_names:
      raise ValueError("Attempted to use reserved name! Cannot use: " + player2)
    if player1 is None:
      player1 = "Computer1"
    if player2 is None:
      player2 = "Computer2"
    if player1 == player2:
      raise ValueError("Player names cannot be the same")
    
    # State initialization
    self.players = [player1, player2]
    self.scores = { player1: 0, player2: 0 }
    self.board = None
    self.winner = None
    self.current_player = None
    self.current_player_index = None
    self.game_over = False

    self.COLUMNS = 7
    self.ROWS = 6

  def start_game(self) -> List[List[str]]:
    """ Start a new game of Connect 4.

    Clears the board and chooses a random player to start the game. To check
    which player should play, call `get_current_player()`.
    
    Returns:
      list: A 2-dimensional List representing the cleared game board, with each cell
      equal to None since it is empty. The board is 6 cells tall and 7 cells wide.
      Since it is a 2-D List, board[0][0] refers to the bottom-leftmost cell on
      the board.
    """
    self.board = [[None] * self.COLUMNS for _ in range(self.ROWS)]
    self.current_player_index = random.randint(0, 1)
    self.current_player = self.players[self.current_player_index]
    self.game_over = False
    self.winner = None
    return copy.deepcopy(self.board)

  def place_token(self, column: Optional[int] = None) -> List[List[str]]:
    """Place a token in the given column, for the current player.

    Places a token in the given column for the current player.

    Args:
      column: The column to place the token in.
    
    Returns:
      list: A 2-dimensional List representing the game board after the token has been
      placed. Each element in the List is a string with the name of the player
      who owns the token, or None if there is no token in that position.

    Raises:
      ValueError: If the given column is not a valid column, if the column is not
                  specified and the current player is a human player, or if 
                  the column is specified and the current player is a computer 
                  player.
      RuntimeError: If the game is already over.
    """
    if self.is_game_over():
      raise RuntimeError("Game is over")
    if self.is_current_player_computer() and column is not None:
      raise ValueError("Cannot specify column for computer player!")
    if not self.is_current_player_computer():
      if column is None:
        raise ValueError("Must specify column for human player!")
      elif not self.is_placement_valid(column):
        raise ValueError("Cannot place token in that column: " + column)

    player = self.current_player
    if self.is_current_player_computer():
      # Computer player
      # Select random column
      column = random.randint(0, self.COLUMNS - 1)
      while not self.is_placement_valid(column):
        column = random.randint(0, self.COLUMNS - 1)

    # Find which row to place the token
    row = -1
    for i in range(self.ROWS):
      if self.board[i][column] is None:
        self.board[i][column] = player
        row = i
        break

    if self.__check_win(row, column):
      # Check if token placement triggers a win.
      self.game_over = True
      self.winner = player
      self.scores[player] += 1
    else:
      # Check if game board is filled
      filled = True
      for i in range(self.ROWS):
        for j in range(self.COLUMNS):
          cell = self.board[i][j]
          if cell is None:
            filled = False
            break
        if not filled:
          break
      # If filled, game is over
      if filled:
        self.game_over = True

    self.current_player_index = (self.current_player_index + 1) % 2
    self.current_player = self.players[self.current_player_index]

    return copy.deepcopy(self.board)

  def __check_win(self, row: int, column: int) -> bool:
    """Checks if a win has occurred in the given position.

    Checks the surrounding tiles to see if a Connect4 win has occured in the
    given position. This method checks the horizontal, vertical, and diagonal
    directions.

    Args:
      row: The row of the position to check.
      column: The column of the position to check.
    
    Returns:
      bool: True if a win has occurred in the given position, False otherwise.
    """
    player = self.board[row][column]
    if player is None:
      return False

    return (self.__has_vertical_win(row, column) or 
      self.__has_horizontal_win(row, column) or
      self.__has_diagonal_win(row, column))

  def __has_vertical_win(self, row: int, column: int) -> bool:
    """Check if a vertical win has occurred in the given position.

    Checks the vertical direction for a win in the given position.

    Args:
      row: The row of the position to check.
      column: The column of the position to check.
    
    Returns:
      bool: True if a win has occurred in the given position, False otherwise.
    """
    player = self.board[row][column]
    if player is None:
      return False
    
    top = row
    bottom = row
    for i in range(row, self.ROWS):
      if self.board[i][column] != player:
        break
      top = max(top, i)
    for i in range(row, -1, -1):
      if self.board[i][column] != player:
        break
      bottom = min(bottom, i)
    if top - bottom + 1 >= 4:
      # Vertical line of length >= 4
      return True

  def __has_horizontal_win(self, row: int, column: int) -> bool:
    """Check if a vertical win has occurred in the given position.

    Checks the vertical direction for a win in the given position.

    Args:
      row: The row of the position to check.
      column: The column of the position to check.
    
    Returns:
      bool: True if a win has occurred in the given position, False otherwise.
    """
    player = self.board[row][column]
    if player is None:
      return False
    
    left = column
    right = column
    for i in range(column, -1, -1):
      if self.board[row][i] != player:
        break
      left = min(left, i)
    for i in range(column, self.COLUMNS):
      if self.board[row][i] != player:
        break
      right = max(right, i)
    if right - left + 1 >= 4:
      # Horizontal line of length >= 4
      return True

  def __has_diagonal_win(self, row: int, column: int) -> bool:
    """Check if a diagonal win has occurred in the given position.

    Checks the diagonal directions for a win in the given position.

    Args:
      row: The row of the position to check.
      column: The column of the position to check.
    
    Returns:
      bool: True if a win has occurred in the given position, False otherwise.
    """
    player = self.board[row][column]
    if player is None:
      return False
    
    # Check top left to bottom right diagonal
    top_left = (row, column)
    bottom_right = (row, column)
    while True:
      new_row, new_column = top_left[0] - 1, top_left[1] - 1
      if (new_row < 0 or new_row >= self.ROWS) or \
        (new_column < 0 or new_column >= self.COLUMNS):
        # Out of bounds
        break
      if self.board[new_row][new_column] != player:
        break
      top_left = (new_row, new_column)
    while True:
      new_row, new_column = bottom_right[0] + 1, bottom_right[1] + 1
      if (new_row < 0 or new_row >= self.ROWS) or \
        (new_column < 0 or new_column >= self.COLUMNS):
        # Out of bounds
        break
      if self.board[new_row][new_column] != player:
        break
      bottom_right = (new_row, new_column)
    if bottom_right[0] - top_left[0] + 1 >= 4:
      # Top left to bottom right diagonal of length >= 4
      return True
    
    # Check top right to bottom left diagonal
    top_right = (row, column)
    bottom_left = (row, column)
    while True:
      new_row, new_column = top_right[0] - 1, top_right[1] + 1
      if (new_row < 0 or new_row >= self.ROWS) or \
        (new_column < 0 or new_column >= self.COLUMNS):
        # Out of bounds
        break
      if self.board[new_row][new_column] != player:
        break
      top_right = (new_row, new_column)
    while True:
      new_row, new_column = bottom_left[0] + 1, bottom_left[1] - 1
      if (new_row < 0 or new_row >= self.ROWS) or \
        (new_column < 0 or new_column >= self.COLUMNS):
        # Out of bounds
        break
      if self.board[new_row][new_column] != player:
        break
      bottom_left = (new_row, new_column)
    if bottom_left[0] - top_right[0] + 1 >= 4:
      # Top right to bottom left diagonal of length >= 4
      return True
    
    # No line of length 4 found
    return False

  def get_scores(self) -> Dict[str, int]:
    """ Get the scores of the players.

    Get the current tally of player scores. Each time a player wins a game, their score 
    increases by 1. 

    Returns:
      dict: A dictionary with the names of each player as the keys and the scores as
      the values.
    """
    return copy.deepcopy(self.scores)
    

  def get_winner(self) -> str: 
    """ Get the name of the winner.
    If the game ends without a winner, 'None' will be used. 

    Returns: 
      str: The name of the winning player. Otherwise, None. 
    """
    return self.winner  

  def get_current_player(self) -> str:
    """ Get the name of the player that must place a token to 
    advance the game.  

    Returns: 
      str: The name of the player on move. 
    """
    return self.current_player 

  def is_current_player_computer(self) -> bool:
    """ Check if the current player is the computer. 
    Meaning the computer must place a token to advance the game.  

    Returns:
      bool: True if the player on move is a computer, False otherwise. 
    """
    if (self.current_player == 'Computer1' or
        self.current_player == 'Computer2'):
        return True
    return False 

  def get_player_names(self) -> list:
    """ Get the name of the players. 
    If the game was initiated without player names then Computer1 and Computer2 
    will be used. 

    Returns:
      list: The names of the players.
    """
    return copy.deepcopy(self.players)

  def is_game_over(self) -> bool:
    """ Check if the game has ended. 
    The game has ended if no more valid moves can be made.
    
    Returns: 
      bool: True if the game ended, False otherwise. 
    """
    return self.game_over 

  def is_placement_valid(self, column: int) -> bool: 
    """ Check if the move is valid. 
    A move is valid if the game has started and a token can be placed in the 
    specified column number. 
    Column number 0 is the left-most column. 

    Args: 
      column_number (int): The number of the column in the range of 0 to 6.

    Returns: 
      bool: True if the move is valid, False otherwise.

    """
    if self.board != None and column != None: 
      if column < 0 or column >= self.COLUMNS:
        return False
      for i in range(self.ROWS - 1, -1, -1):
        if self.board[i][column] is None:
          return True
    return False
