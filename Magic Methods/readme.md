Python 的“魔术方法”（Magic Methods）在英文中通常被称为 Magic Methods，或者更通俗地被称为 Dunder Methods（即 Double Underscore Methods，双下划线方法），因为它们总是以双下划线开头和结尾

## new和init

在 Python 的面向对象编程中，`__new__` 和 `__init__` 是两个负责“生孩子”的关键魔术方法，但它们的分工完全不同。

简单来说：**`__new__` 负责“制造”对象，`__init__` 负责“装修”对象。**

---

### 1. `__new__`：构造器 (The Constructor)

它是**真正创建实例**的方法。

* **调用时机**：在 `__init__` 之前被调用。
* **参数**：第一个参数是 `cls`（类本身），因为它在实例存在之前执行。
* **返回值**：**必须返回一个实例**。通常调用父类的 `super().__new__(cls)` 来创建并返回实例。
* **作用**：分配内存，创建一个空对象。

### 2. `__init__`：初始化器 (The Initializer)

它是**配置实例**的方法。

* **调用时机**：在 `__new__` 返回实例之后被调用。
* **参数**：第一个参数是 `self`（即 `__new__` 刚刚创建好的那个实例）。
* **返回值**：**必须返回 `None**`。如果返回其他值会报错。
* **作用**：给对象设置属性，进行初始化设置。

---

### 核心区别对比

| 特性 | `__new__` | `__init__` |
| --- | --- | --- |
| **类型** | 静态方法 (Static Method) - 尽管不需要 `@staticmethod` 装饰器 | 实例方法 (Instance Method) |
| **主要职责** | **创建**对象 (Create) | **初始化**对象 (Initialize) |
| **第一个参数** | `cls` (类) | `self` (实例) |
| **返回值** | **必须返回实例** | **必须返回 None** |
| **常见程度** | 极少重写 (仅在特殊场景) | 几乎每个类都重写 |

---

### 执行流程演示

这段代码清楚地展示了先后顺序：

```python
class Person:
    def __new__(cls, name):
        print(f"1. __new__ 被调用: 正在为类 {cls.__name__} 创建对象...")
        # 调用父类(object)的 __new__ 方法来真正创建对象
        instance = super().__new__(cls)
        # 此时 instance 已经存在，但还未初始化
        return instance

    def __init__(self, name):
        print("2. __init__ 被调用: 正在初始化对象属性...")
        self.name = name

# 实例化
p = Person("Gemini")

# 输出:
# 1. __new__ 被调用: 正在为类 Person 创建对象...
# 2. __init__ 被调用: 正在初始化对象属性...

```

### 关键机制：二者的联系

`__init__` 是由 `__new__` 触发的，但有一个前提条件：

> 只有当 `__new__` 返回了**当前类 (`cls`) 的实例**时，Python 解释器才会自动调用 `__init__`。

如果 `__new__` 返回了 `None` 或者其他类的实例，`__init__` **不会**被执行。

```python
class Silent:
    def __new__(cls):
        print("New 执行了")
        return None # 故意不返回实例

    def __init__(self):
        print("Init 执行了") # 这行永远不会打印

s = Silent()
# 输出: New 执行了

```

---

### 什么时候需要重写 `__new__`？

你平时 99% 的时间只需要写 `__init__`。只有在以下两种高级场景下，才需要动用 `__new__`：

#### 1. 继承不可变类型 (Immutable Types)

例如 `int`, `str`, `tuple`。因为它们是不可变的，一旦创建就无法修改。所以你不能在 `__init__` 里修改它们的值，必须在创建时（`__new__`）就决定好。

**例子：定义一个永远为正数的整数类**

```python
class PositiveInt(int):
    def __new__(cls, value):
        # 在创建 int 实例之前，先对 value 进行处理
        value = abs(value) 
        return super().__new__(cls, value)

    # 这里写 __init__ 是没用的，因为 int 一旦由 __new__ 创建，数值就定死了

i = PositiveInt(-10)
print(i) # 输出 10

```

#### 2. 单例模式 (Singleton Pattern)

确保一个类在程序运行期间只有一个实例。

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # 如果没有实例，就创建一个
            cls._instance = super().__new__(cls)
        # 如果已经有了，直接返回之前的那个
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)  # True (它们是同一个对象)

```

### 总结

* **`__new__`** 是**生母**，负责把孩子生出来（分配内存）。
* **`__init__`** 是**保姆**，负责给孩子穿衣喂饭（赋值属性）。

**下一步可以为你做的：**
你需要我展示如何用 `__new__` 来实现一个更复杂的“单例模式”（例如线程安全的单例），或者解释一下 Python 的元类（Metaclass）是如何控制 `__new__` 的吗？