class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = (x ** 2 + y ** 2) ** 0.5

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __iter__(self):
        return iter((self.x, self.y))

    def __str__(self):
        return f'Vector({self.x}, {self.y})'

    def normalize(self):
        return Vector(self.x / self.length, self.y / self.length)
