import math

class Error(Exception):
    def __init__(self, message):
        super().__init__(message)

class Vector2D:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return self.__repr__()

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f'(V({self.x},{self.y}))'

    def dot(self, other):
        if not isinstance(other, Vector2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y
    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def __getitem__(self, idx):
        match (idx):
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise Error('Invalid index')
    
    def __setitem__(self, idx, val):
        match (idx):
            case 0:
                self.x = val
            case 1:
                self.y = val
            case _:
                raise Error('Invalid index')

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Vector addition."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """Multiplication of a vector by a scalar."""

        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vector2D(self.x*scalar, self.y*scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar):
        """Reflected multiplication so vector * scalar also works."""
        return self.__mul__(scalar)

    def __neg__(self):
        """Negation of the vector (invert through origin.)"""
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar):
        """True division of the vector by a scalar."""
        return Vector2D(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar):
        """True division of the vector by a scalar."""
        return Vector2D(self.x // scalar, self.y // scalar)

    def __mod__(self, scalar):
        """One way to implement modulus operation: for each component."""
        return Vector2D(self.x % scalar, self.y % scalar)

    def __abs__(self):
        """Absolute value (magnitude) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, other):
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self):
        """Return the vector's components in polar coordinates."""
        return self.__abs__(), math.atan2(self.y, self.x)
