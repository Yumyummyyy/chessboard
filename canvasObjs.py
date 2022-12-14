try:
    import tkinter as tk
except ImportError: # python2
    import Tkinter as tk
import math
from globals import globals
from pos import Scale, Pos
import config
from abc import ABC, abstractmethod
from PIL import Image, ImageTk

class AbsObj(ABC): # pos is in px, scale is relative i.e. 0 to 10
    def __init__(self, scale=None, size=None):
        if scale == None:
            scale = Pos(0, 0)
        self.scale = scale
        if size != None:
            self.size = size
        self.obj = self.createObj()

    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def createObj(self):
        pass

    @property
    def pos(self):
        return globals.canvas.toActual(self.scale)
    @property
    def end(self):
        return globals.canvas.toActual(self.scale + self.size)
    @property
    def center(self):
        return Scale(self.scale.x + self.size.x/2, self.scale.y + self.size.y/2)

    def delete(self):
        globals.canvas.canvas.delete(self.obj)

class Rect(AbsObj):
    def __init__(self, scale, size, fill, activeFill=None, outline=None):
        if outline == None:
            outline = fill
        self.color = fill
        self.activeColor = activeFill
        self.outline = outline
        super().__init__(scale, size)
    def createObj(self):
        return globals.canvas.canvas.create_rectangle(
            self.pos.x,
            self.pos.y,
            self.end.x,
            self.end.y,
            fill=self.color,
            activefill=self.activeColor,
            outline=self.outline
        )
    def update(self):
        globals.canvas.canvas.coords(self.obj, self.pos.x, self.pos.y, self.end.x, self.end.y)
    def getSize(self):
        return self.size

class Text(AbsObj):
    def __init__(self, scale, fontSize, text, centerPoint=None, color="black"):
        self._text = text
        self.centerPoint = centerPoint
        self.fontSize = globals.canvas.getScaleFromFontSize(fontSize)
        self.color = color
        super().__init__(scale, None)
        self.text = text
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text):
        self._text = text
        globals.canvas.canvas.itemconfig(self.obj, text=text)
        if self.centerPoint:
            self.moveto(globals.canvas.centerOf(globals.canvas.toScale(self.size), self.centerPoint))
    @property
    def size(self):
        bounds = globals.canvas.canvas.bbox(self.obj)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        return Pos(width, height)
    def getScaledFontSize(self):
        # return math.ceil(self.fontSize * (globals.canvas.getDimensions().x + globals.canvas.getDimensions().y) / 2)
        return math.ceil(self.fontSize * globals.canvas.getDimensions().x)
    def createObj(self): # because yes
        pos = self.pos
        return globals.canvas.canvas.create_text(pos.x, pos.y, text=self.text, fill=self.color, font=(config.FONT, self.getScaledFontSize()))
    def snap(self):
        if self.centerPoint:
            self.moveto(globals.canvas.centerOf(globals.canvas.toScale(self.size), self.centerPoint))
            return
        self.moveto()
    def moveto(self, scale=None):
        if scale == None:
            scale = self.scale
        elif type(scale) == Scale:
            self.scale = scale
        globals.canvas.canvas.moveto(self.obj, self.pos.x, self.pos.y)
    def update(self):
        globals.canvas.canvas.itemconfig(self.obj, font=(config.FONT, self.getScaledFontSize()))
        self.moveto()

# scale refers to relative position
class Button: # a button on tk canvas because yes
    def __init__(self, clickFunc, scale, size, fill, activeFill, fontSize, text):
        self.bg = Rect(scale, size, fill=fill)
        self.fill = fill
        self.activeFill = activeFill
        self.text = Text(None, fontSize, text, centerPoint=self.bg.center)
        self.click = clickFunc
        self.update()
        self.bindEvents()
    def moveto(self, scale):
        diff = self.bg.scale - scale
        self.bg.scale = scale
        self.text.scale -= diff
        self.update()
    def update(self):
        self.bg.update()
        self.text.update()
        self.text.snap()
    def bindEvent(self, evt, func):
        globals.canvas.canvas.tag_bind(self.bg.obj, evt, func)
        globals.canvas.canvas.tag_bind(self.text.obj, evt, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)
        # globals.canvas.canvas.tag_bind(self.bg.obj, "<Enter>", self.highlight)
        # globals.canvas.canvas.tag_bind(self.bg.obj, "<Leave>", self.unhighlight)
        self.bindEvent("<Enter>", self.highlight)
        self.bindEvent("<Leave>", self.unhighlight)
    def highlight(self, e):
        globals.canvas.canvas.itemconfig(self.bg.obj, fill=self.activeFill, outline=self.activeFill)
    def unhighlight(self, e):
        globals.canvas.canvas.itemconfig(self.bg.obj, fill=self.fill, outline=self.fill)
    def delete(self):
        globals.canvas.canvas.tag_unbind(self.bg.obj, "<Button-1>")
        globals.canvas.canvas.tag_unbind(self.text.obj, "<Button-1>")
        self.bg.delete()
        self.text.delete()
