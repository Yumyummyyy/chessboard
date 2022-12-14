import math
import config

class Pos(): # actual pos
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"[{str(self.x)} {str(self.y)}]"
    def __sub__(self, other):
        other = self.isValid(other)
        return type(self)(self.x - other.x, self.y - other.y)
    def __rsub__(self, other):
        return type(self)(other, other) - self
    def __add__(self, other):
        other = self.isValid(other)
        return type(self)(self.x + other.x, self.y + other.y)
    def __truediv__(self, other):
        other = self.isValid(other)
        return type(self)(self.x / other.x, self.y / other.y)
    def __mul__(self, other):
        other = self.isValid(other)
        return type(self)(self.x * other.x, self.y * other.y)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __round__(self, ndigits=0):
        return type(self)(round(self.x, ndigits), round(self.y, ndigits))
    def __floor__(self):
        return type(self)(math.floor(self.x), math.floor(self.y))
    def __le__(self, other):
        other = self.isValid(other)
        return self.x <= other.x and self.y <= other.y
    def __ge__(self, other):
        other = self.isValid(other)
        return self.x >= other.x and self.y >= other.y
    def __eq__(self, other):
        return type(self) == type(other) and self.x == other.x and self.y == other.y
    def __deepcopy__(self, other):
        return type(self)(self.x, self.y)
    def __hash__(self):
        return hash((self.x, self.y))
    def inside(self, start, end):
        return start <= self <= end
    def isValid(self, other): # check if variable is of same class
        isPos = isinstance(other, type(self))
        isNum = isinstance(other, int) or isinstance(other, float)
        if not isPos and not isNum:
            raise TypeError(f"Second variable operating is not of class {type(self)} but is of type {type(other)}")
        if isNum:
            return type(self)(other, other)
        return other

class BoardPos(Pos): # board pos
    def exceedsBoard(self):
        more = self.x >= config.BOARD_LENGTH or self.y >= config.BOARD_LENGTH
        less = self.x < 0 or self.y < 0
        if more or less:
            return True
        return False

class Scale(Pos):
    def __init__(self, x=None, y=None):
        # if not (0 <= x <= 1) or not (0 <= y <= 1):
            # raise ValueError("Scale can only be between 0 and 1")
        super().__init__(x, y)
