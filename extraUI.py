import tkinter as tk
import config
from piece import PieceImg
from pos import Pos
from globals import globals

WIDTH = 40
MARGIN = -7

class TakenPieces:
    def __init__(self, color, startPos):
        self.color = color
        self.yAxis = startPos.y - WIDTH + 15
        boardWidth = config.BOARD_LENGTH * config.SQUARE_LENGTH
        if self.color == config.Color.black:
            self.yAxis = startPos.y + boardWidth + WIDTH
        self.imgs = []
    def update(self):
        startPos = Pos(globals.board.startPos.x - 10, self.yAxis)
        self.imgs = []
        for piece in globals.board.taken.getTable(self.color):
            img = PieceImg(self.color, piece.imgName)
            img.resize(WIDTH)
            img.moveto(startPos)
            self.imgs.append(img)
            startPos += Pos(WIDTH + MARGIN, 0)

class Menu:
    def __init__(self):
        pass

class extraUI:
    def __init__(self, startPos):
        self.takenPieces = {
            config.Color.white: TakenPieces(config.Color.white, startPos),
            config.Color.black: TakenPieces(config.Color.black, startPos),
        }
        self.menu = Menu()
