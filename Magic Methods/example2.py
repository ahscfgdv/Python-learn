# %%
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}"

    def __eq__(self, value) -> bool:
        print("__eq__ called")
        return (
            self.year == value.year
            and self.month == value.month
            and self.day == value.day
        )

    def __ne__(self, value) -> bool:
        print("__ne__ called")
        return (
            self.year != value.year
            or self.month != value.month
            or self.day != value.day
        )

    def __lt__(self, value) -> bool:
        print("__lt__ called")
        if self.year < value.year:
            return True
        elif self.year == value.year:
            if self.month < value.month:
                return True
            elif self.month == value.month:
                return self.day < value.day
        return False


a = Date(2024, 6, 18)
b = Date(2024, 6, 18)

# 没有定义eq函数
# print(a is y)
# 结果是false
# a.__eq__(b)
print(a == b)
# 如果没有定义不等于函数，结果为eq函数取反
print(a != b)
# python没有默认的大于实现
print(a < b)


#%%
class Date2:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def __repr__(self) -> str:
        return f"Date2({self.year}, {self.month}, {self.day})"
    
    def __eq__(self, value) -> bool:
        print("__eq__ called")
        return (
            self.year == value.year
            and self.month == value.month
            and self.day == value.day
        )
    
    def __hash__(self) -> int:
        print("__hash__ called")
        return hash((self.year, self.month, self.day))
        
x =  Date2(2024, 6, 18)
y =  Date2(2024, 6, 18)
income = {}
income[x] = 1000
income[y] = 1000
# 当定义了__eq__函数后，必须定义__hash__函数，否则对象不可哈希  
# hash函数必须返回整数，相等的对象必须有相同的哈希值
print(income)
# %%
class Date3():
    def __init__(self, year, month, day) -> None:
        self.year = year
        self.month = month
        self.day = day
    
    def __bool__(self) -> bool:
        print("__bool__ called")
        return False
    

x = Date3(2024, 6, 18)

print(bool(x))

if x:
    print("True")    
    

# %%
