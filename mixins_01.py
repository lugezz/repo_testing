class A:
    total = 12345


class B(A):
    pass


class C(A):
    pass


class M:
    def get_total(self):
        return self.total


class D(B, M):
    pass


class E(C, M):
    pass


d = D()
e = E()

print(d.get_total())
print(e.get_total())
