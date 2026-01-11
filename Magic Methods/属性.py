# %%
from typing import Any


class A:
    def __init__(self):
        self.exist = "asd"
        self.count = 0

    # 只用于访问不存在的属性
    def __getattr__(self, name):
        print(f"__getattr__ called for {name}")
        return None

    def __getattribute__(self, name: str) -> Any:
        print(f"__getattribute__ called for {name}")
        # self.count += 1 会导致无限递归,因为每次访问self.count都会调用__getattribute__
        # 使用默认实现避免无限递归
        return super().__getattribute__(name)


o = A()
print(o.exist)
print(o.not_exist)


# %%
class B:
    def __init__(self):
        self.exist = "asd"
        self.count = 0

    def __setattr__(self, name: str, value: Any) -> None:
        print(f"__setattr__ called for {name} with value {value}")
        # 使用默认实现避免无限递归
        super().__setattr__(name, value)


o = B()
print(o.exist)


# %%
class C:
    _attr = {}

    def __init__(self):
        self.exist = "asd"

    def __setattr__(self, name: str, value: Any) -> None:
        self._attr[name] = value

    def __getattr__(self, name: str) -> Any:
        if name not in self._attr:
            raise AttributeError(f"{name} not found")
        return self._attr[name]


o1 = C()
o2 = C()
o1.exist = "value1"
print(o2.exist)


# %%
class D:
    def __init__(self):
        self.data = "asd"

    def __delattr__(self, name: str) -> None:
        print(f"__delattr__ called for {name}")
        super().__delattr__(name)


o = D()
del o.data
print(o.data)


# %%
class E:
    def __init__(self):
        self.data = "asd"

    def __dir__(self):
        lst = super().__dir__()
        return [el for el in lst if not el.startswith("_")]


o = E()
print(dir(o))


# %%
class F:
    def __get__(self, obj, onwer=None):
        print(obj, onwer)
        return 0


class G:
    x = F()


o = G()
print(o.x)


# %%
class H:
    # 规定类中所能包含的属性
    __slots__ = ["a", "b"]


o = H()
o.a = 10
# %%
