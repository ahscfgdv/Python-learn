# %%
import re
from typing import Self


class A:
    # 对象创建时调用
    def __new__(cls, x):
        print("__new__ called")
        return super().__new__(cls)

    # 对象创建后返回实例调用
    def __init__(self, x) -> None:
        print("__init__ called")
        self.x = x


o = A(10)
# obj = __new__(A,10)
# __init__(obj,10)


# %%
import sys

class B:
    # 对象销毁时调用
    def __del__(self) -> None:
        print("__del__ called")


o = B()
x = o
print(f"当前引用计数: {sys.getrefcount(o) - 1}") # 通常显示 2 (o 和 x)

del o

print("finish")

"""
正常执行结果
finfish
__del__ called
当del o调用时还存在x对o的引用，因此不会立即调用__del__方法
先打印finish

当使用jupyter运行时，o对象不会立刻被回收而是保存在jupyter内核中
结果为
__del__ called
finish
"""


# %%
class C:
    # 对象被打印时调用
    # 提供可读性更好的字符串表示
    def __str__(self) -> str:
        return "C() str"
    
    # 提供更详细的字符串表示
    def __repr__(self) -> str:
        return "C() repr"
    
o = C()
print(o)          # 调用 __str__
print(repr(o))   # 调用 __repr__
# 当没有str函数时会调用repr函数
# %%
class D:
    def __format__(self, format_spec: str) -> str:
        if format_spec == "x":
            return "D() in format x"
        return "D()"

o = D()
print(f"{o:x}")  # 调用 __format__ 方法，format_spec 为 "
    

# %%
class E:
    def __bytes__(self) -> bytes:
        print("__bytes__ called")
        return b"E() in bytes"
    
o = E()
b = print(bytes(o))  # 调用 __bytes__ 方法
# %%

