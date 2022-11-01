import tkinter as tk
from pos import BoardPos
from globals import globals
import config
import pieces
import draw
from piece import Piece
canvas, board = globals.canvas, globals.board

pieceTypes = [ # name of images of pieces that can pawn can promote to
    pieces.Queen,
    pieces.Rook,
    pieces.Bishop,
    pieces.Knight,
]

class PromotionPiece:
    def __init__(self, squareImgObj, pieceImg, pieceImgObj, pieceType, prompt):
        self.squareImgObj = squareImgObj
        self.pieceImg = pieceImg
        self.pieceImgObj = pieceImgObj
        self.pieceType = pieceType
        self.prompt = prompt
        self.bindEvents()
    def click(self, e):
        globals.board.movePiece(self.prompt.toMoveTo, self.prompt.promotingPawn)
        square = self.prompt.promotingPawn.square
        color = self.prompt.promotingPawn.color
        self.prompt.promotingPawn.delete()
        self.pieceType(square.boardPos, color)
        self.prompt.delete()
        self.prompt = None # prevent circular reference between PromotionPiece and PromotionPrompt
    def bindEvent(self, event, func):
        globals.canvas.tag_bind(self.pieceImgObj, event, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)


class PromotionPrompt:
    def __init__(self, piece, toMoveTo):
        self.squares = []
        self.promotingPawn = globals.board.getSquare(piece.boardPos).piece
        self.toMoveTo = toMoveTo
        increment = BoardPos(0, -1)
        if piece.color == config.Color.white:
            increment *= -1
        for pieceType in pieceTypes:
            startPos = globals.board.getPosFromBoardPos(toMoveTo)
            squareImgObj = self.drawSquare(startPos)
            img = pieceType.getImg(piece.color, pieceType.imgName)
            imgObj = pieceType.getImgObj(img)
            globals.canvas.moveto(imgObj, startPos.x, startPos.y)
            self.squares.append(PromotionPiece(squareImgObj, img, imgObj, pieceType, self))
            toMoveTo += increment
        self.funcId = globals.canvas.bind("<ButtonRelease-1>", self.release)
    def release(self, e):
        globals.canvas.unbind("<ButtonRelease-1>", self.funcId)
        self.funcId = globals.canvas.bind("<Button-1>", self.cancel)
    def cancel(self, e):
        globals.canvas.unbind("<Button-1>", self.funcId)
        self.delete()
    def delete(self):
        for square in self.squares:
            globals.canvas.delete(square.squareImgObj)
            globals.canvas.delete(square.pieceImgObj)
    def drawSquare(self, startPos):
        return globals.canvas.create_rectangle(
            startPos.x,
            startPos.y,
            startPos.x + config.SQUARE_LENGTH,
            startPos.y + config.SQUARE_LENGTH,
            outline=draw.WHITE,
            fill=draw.WHITE,
            width=5,
        )