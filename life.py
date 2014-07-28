# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 19:49:39 2014

@author: brian
"""

import socket, time, re

class LifeBoard:
  """
  Play the game of life
  """
  
  def __init__(self, board):
    """
    board - 2d array of the board where '*' is an alive cell and ' ' is a dead 
      cell
    """
    self.board = board
    
  def iterate(self,count=1):
    for i in range(count):
      newboard = ["" for x in range(len(self.board))]
      for row in range(len(board)):
        for col in range(len(board[row])):
          neighbors = self._getval(row-1,col-1) + self._getval(row-1,col) + self._getval(row-1,col+1)+ \
                      self._getval(row,col-1) + self._getval(row,col+1)+ \
                      self._getval(row+1,col-1) + self._getval(row+1,col) + self._getval(row+1,col+1)
    
          if neighbors < 2 or neighbors > 3:
            newboard[row] += ' '
          elif neighbors == 3 or (neighbors == 2 and self._getval(row, col) == 1):
            newboard[row] += '*'
          else:
            newboard[row] += ' '
      self.board = newboard
    
  def _getval(self, row,col):
    if row < 0 or col < 0:
      return 0
    try:    
      return 1 if self.board[row][col] == '*' else 0
    except IndexError:
      return 0

        
host = '127.0.0.1'
port = int(raw_input("enter port"))      
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
data = s.recv(4096)
data = data[102:]

try:
  while(True):
    regex = re.compile("(\d*) Generations")
    r = regex.search(data)
    
    board = [i[1:-1] for i in data.split('\n')[3:-2]]
        
    lb = LifeBoard(board)
    lb.iterate(count=int(r.groups(0)[0]))
    res_board = lb.board
    
    res_board.insert(0, '#'*(len(board[0])+1))
    res_board.append('#'*(len(board[0])+1)+'\n')
    print('#\n#'.join(res_board)) 
    s.send('#\n#'.join(res_board))
    data = s.recv(4096)
except:
  print(data)