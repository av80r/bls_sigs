import params
from fields import Fq, Fq2


class g1:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

        if self.is_infinity():
            self.X = self.basefield.zero()
            self.Y = self.basefield.one()

    def __str__(self):
        if self.is_infinity():
            return 'Infinity'
        return 'X = ' + str(self.X) + ', Y = ' + str(self.Y) + ', Z = ' + str(self.Z)

    def __neg__(self):
        if not self.is_infinity():
            return g1(self.X, - self.Y, self.Z)
        return self

    def __add__(self, other):
        '''
        These check are included for the sake of completeness.
        In reality, these cases will never be reached and thus could be commited
        '''
        # Addition is trivial when one of the points is infinity:
        if self.is_infinity():
            return other
        elif other.is_infinity():
            return self
        # If the point is being added to itself, just double instead
        elif self == other:
            return self.double()

        # http://www.hyperelliptic.org/EFD/g1p/auto-shortw-jacobian-0.html#addition-add-2007-bl
        Z1Z1 = self.Z.square()
        Z2Z2 = other.Z.square()
        U1 = self.X * Z2Z2
        U2 = other.X * Z1Z1
        S1 = self.Y * other.Z * Z2Z2
        S2 = other.Y * self.Z * Z1Z1
        H = U2 - U1
        I = (2 * H).square()
        J = H * I
        r = 2 * (S2-S1)
        V = U1*I
        X3 = r.square() - J - (2 * V)
        Y3 = r * (V-X3) - (2 * S1 * J)
        Z3 = ((self.Z + other.Z).square() - Z1Z1 - Z2Z2) * H
        return g1(X3, Y3, Z3)

    def __sub__(self, other):
        return self + other.__neg__()

    def __rsub__(self, other):
        return other + self.__neg__()

    def __mul__(self, other=int):
        # Basic Double and Add alg:
        # Todo: Make constant time(ish)
        # Definatly not constant time crypto!
        other = bin(other)
        other = other[3:]  # Removes '0b1' from number
        res = self
        for i in other:
            res = res.double()
            if i == '1':
                res += self
        return res

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.as_affine() == other.as_affine()

    def double(self):
        if self.is_infinity():
            # Doubling infinity is trivial
            return self
        # http://www.hyperelliptic.org/EFD/g1p/auto-shortw-jacobian-0.html#doubling-dbl-2009-l
        A = self.X.square()
        B = self.Y.square()
        C = B.square()
        D = 2 * ((self.X + B).square() - A - C)
        E = 3 * A
        F = E.square()
        X3 = F - 2 * D
        Y3 = E * (D - X3) - 8 * C
        Z3 = 2 * self.Y * self.Z
        return g1(X3, Y3, Z3)

    def is_infinity(self):
        return self.Z.is_zero()

    def is_on_curve(self):
        if self.is_infinity():
            return True
        return self.Y**2 == self.X**3 + params.b*(self.Z**6)

    def as_affine(self):
        return self.x, self.y, self.is_infinity()

    @property
    def x(self):
        return self.X * (self.Z**2).inverse()

    @property
    def y(self):
        return self.Y * (self.Z**3).inverse()

    @property
    def basefield(self):
        return self.X.zero()

    @classmethod
    def from_affine(cls, x, y, infinity=False):
        if infinity:
            return cls(x, y, x.zero())
        return cls(x, y, x.one())

    @classmethod
    def get_point_from_x(cls, X, greatest=False):
        X3b = X ** 3 + params.b
        Y = X3b.sqrt()
        if greatest and Y < - Y:
            Y = - Y
        return cls(X, Y, X.one())


if __name__ == '__main__':
    A = g1.get_point_from_x(Fq2(Fq(4, 19), Fq(6, 19)), True)
    B = g1.get_point_from_x(Fq2(Fq(7, 19), Fq(11, 19)), True)

    print((A-A).is_infinity())
    print((B * 7) == (B+B+B+B+B+B+B))
