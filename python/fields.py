class Fq(int):
    def __new__(cls, x: int, q: int):
        x = x % q
        ret = super().__new__(cls, x)
        ret.q = q
        return ret

    def __str__(self):
        return super().__str__()

    def __add__(self, other):
        return Fq(super().__add__(other), self.q)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Fq(super().__neg__(), self.q)

    def __sub__(self, other):
        return Fq(super().__sub__(other), self.q)

    def __rsub__(self, other):
        return Fq(super().__sub__(other).__neg__(), self.q)

    def __mul__(self, other):
        return Fq(super().__mul__(other), self.q)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rdiv__(self, other):
        return Fq(other * self.inverse(), self.q)

    def __pow__(self, power):
        # Basic square and multiply algorithm
        power = bin(int(power))
        power = power[3:] # Removes '0b1' from number
        ret = self
        for i in power:
            ret *= ret
            if i:
                ret *= self
        return ret

    def inverse(self):
        t = 0
        new_t = 1
        r = self.q
        new_r = self

        while new_r:
            q = r // new_r
            t, new_t = new_t, t - q * new_t
            r, new_r = new_r, r - q * new_r
        return Fq(t, self.q)

    def sqrt(self):
        # Todo: Catch non-existent sqrt
        # Simplified Tonelli-Shanks for q==3 mod 4
        assert self.q % 4 == 3
        return self**((self.q + 1)/4)

    def is_zero(self):
        return self == 0

    def is_one(self):
        return self == 1

    def zero(self):
        return Fq(0, self.q)

    def one(self):
        return Fq(1, self.q)


class Fq2(tuple):
    def __new__(cls, c0: Fq, c1: Fq):
        return super().__new__(cls, (c0, c1))

    def __add__(self, other):
        return Fq2(self[0] + other[0], self[1] + other[1])

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Fq2(self[0].__neg__(), self[1].__neg__())

    def __sub__(self, other):
        return Fq2(self[0]-other[0], self[1] - other[1])

    def __rsub__(self, other):
        return Fq2(other[0] - self[0], other[1] - self[1])

    def __mul__(self, other):
        aa = self[0] * other[0]
        bb = self[1] * other[1]
        o = other[0] + other[1]
        c1 = self[1] + self[0]
        c1 *= o
        c1 -= aa
        c1 -= bb
        c0 = aa - bb
        return Fq2(c0, c1)

    def __pow__(self, power):
        # Basic square and multiply algorithm
        power = bin(int(power))
        power = power[3:] # Removes '0b1' from number
        ret = self
        for i in power:
            ret *= ret
            if i:
                ret *= self
        return ret

    def __str__(self):
        return 'Fq2(' + str(self[0]) + ' + ' + str(self[1]) + ' * u)'

    def mul_by_nonresidue(self):
        return Fq2(self[0] - self[1], self[0] + self[1])

    def inverse(self):
        t1 = self[1] * self[1]
        t0 = self[0] * self[0]
        t0 += t1
        t0 = t0.inverse()
        a = self[0]*t0
        b = self[1]*t0
        b = -b
        return Fq2(a, b)

    def is_zero(self):
        return self[0].is_zero() and self[1].is_zero()

    def is_one(self):
        return self[0].is_one() and self[1].is_zero()

    def zero(self):
        return Fq2(self[0].zero(), self[1].zero())

    def one(self):
        return Fq2(self[0].one(), self[1].zero())

    @property
    def q(self):
        return self[0].q


class Fq6(tuple):
    def __new__(cls, c0, c1, c2):
        return super().__new__(cls, (c0, c1, c2))

    def __neg__(self):
        c0 = -self[0]
        c1 = -self[1]
        c2 = -self[2]
        return Fq6(c0, c1, c2)

    def __add__(self, other):
        c0 = self[0] + other[0]
        c1 = self[1] + other[1]
        c2 = self[2] + other[2]
        return Fq6(c0, c1, c2)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        c0 = self[0] - other[0]
        c1 = self[1] - other[1]
        c2 = self[2] - other[2]
        return Fq6(c0, c1, c2)

    def __rsub__(self, other):
        c0 = other[0] - self[0]
        c1 = other[1] - self[1]
        c2 = other[2] - self[2]
        return Fq6(c0, c1, c2)

    def __mul__(self, other):
        aa = self[0]
        bb = self[1]
        cc = self[2]

        aa *= other[0]
        bb *= other[1]
        cc *= other[2]

        # t1
        t1 = other[1]
        t1 += other[2]
        tmp = self[1] + self[2]
        t1 *= tmp
        t1 -= bb
        t1 -= cc
        t1 = t1.mul_by_nonresidue()
        t1 += aa

        # t3
        t3 = other[0]
        t3 += other[2]
        tmp = self[0] + self[2]
        t3 *= tmp
        t3 -= aa
        t3 += bb
        t3 -= cc

        # t2
        t2 = other[0]
        t2 += other[1]
        tmp = self[0] + self[1]
        t2 *= tmp
        t2 -= aa
        t2 -= bb
        t2 += cc.mul_by_nonresidue()

        return Fq6(t1, t2, t3)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return 'Fq6(' + str(self[0]) + ' + ' + str(self[1]) + ' * v + ' + str(self[2]) + ' * v^2)'

    def inverse(self):
        c0 = self[2]
        c0 = c0.mul_by_nonresidue()
        c0 *= self[1]
        c0 = -c0
        c0 += self[0]*self[0]

        c1 = self[2]
        c1 *= c1
        c1 = c1.mul_by_nonresidue()
        c1 -= self[0]*self[1]

        c2 = self[1]
        c2 = c2*c2
        c2 -= self[0]*self[2]

        tmp1 = self[2]*c1
        tmp2 = self[1]*c2
        tmp1 += tmp2
        tmp1 = tmp1.mul_by_nonresidue()
        tmp2 = self[0]*c0
        tmp1 += tmp2

        tmp1 = tmp1.inverse()
        c0 *= tmp1
        c1 *= tmp1
        c2 *= tmp1
        return Fq6(c0, c1, c2)

    def is_zero(self):
        return self[0].is_zero() and self[1].is_zero() and self[2].is_zero()

    def is_one(self):
        return self[0].is_one() and self[1].is_zero() and self[2].is_zero()

    def mul_by_nonresidue(self):
        c0 = self[2]
        c1 = self[0]
        c2 = self[1]
        c0 = c0.mul_by_nonresidue()
        return Fq6(c0, c1, c2)

    @property
    def q(self):
        return self[0].q


class Fq12(tuple):
    def __new__(cls, c0, c1):
        return super().__new__(cls, (c0, c1))

    def __neg__(self):
        c0 = -self[0]
        c1 = -self[1]
        return Fq12(c0, c1)

    def __add__(self, other):
        c0 = self[0] + other[0]
        c1 = self[1] + other[1]
        return Fq12(c0, c1)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __mul__(self, other):
        aa = self[0] * other[0]
        bb = self[1] * other[1]
        o = other[0] + other[1]
        c1 = self[1] + self[0]
        c1 *= o
        c1 -= aa
        c1 -= bb
        c0 = bb.mul_by_nonresidue()
        c0 += aa
        return Fq12(c0, c1)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rdiv__(self, other):
        return other * self.inverse()

    def __str__(self):
        return 'Fq12(' + str(self[0]) + ' + ' + str(self[1]) + ' * w)'

    def inverse(self):
        c0 = self[0] * self[0]
        c1 = self[1] * self[1]
        c1 = c1.mul_by_nonresidue()
        c0 -= c1

        t = c0.inverse()
        t0 = t * self[0]
        t1 = t * self[1]
        t1 = -t1
        return Fq12(t0, t1)

    def is_zero(self):
        return self[0].is_zero() and self[1].is_zero()

    def is_one(self):
        return self[0].is_one() and self[1].is_zero()

    @property
    def q(self):
        return self[0].q




if __name__ == '__main__':
    # Todo: Replace with proper test cases.
    a = Fq2(Fq(3, 17), Fq(4, 17))
    b = Fq2(Fq(5, 17), Fq(11, 17))
    c = Fq2(Fq(8, 17), Fq(14, 17))

    d = Fq6(a, b, c)
    e = Fq6(c, b, a)

    f = Fq12(d, e)

    # Check inversion in Fq12
    print((f*f.inverse()).is_one())

    # Check sqrt in Fq (q % 4 == 3)
    z = Fq(3, 11)
    print(z.sqrt()*z.sqrt() == z)
