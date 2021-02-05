#!/usr/bin/env python3


class Deco:

    def __init__(self, orig):
        self.orig = orig

    def __call__(self, *args, **kwargs):
        return self.orig(*args, **kwargs)


@Deco
class A:

    pass


class B:

    pass


a = A()
print(type(a))

b = B()
print(type(b))

d = Deco(a)
print(type(d))

d = Deco(b)
print(type(d))
