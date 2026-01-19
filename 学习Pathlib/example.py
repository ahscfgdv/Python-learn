# %%
# Path是一个面向对象的文件系统路径操作模块，有合适的属性和方法
import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
# %%
from pathlib import Path

# 创建 Path 对象（当前目录）
print(Path('.'))  # 相对路径
print(Path.home())  # 用户主目录
print(Path.cwd())  # 当前工作目录

# 创建绝对路径
p = Path('C:/Users/username/Documents/file.txt')  # 绝对路径
p = Path('docs/file.txt')  # 相对路径

# %%
# 使用 / 运算符拼接路径（推荐）
print(Path('/home') / 'user' / 'docs' / 'file.txt')
path = Path.home() / 'Desktop' / 'data.csv'

# 使用 joinpath
path = Path.home().joinpath('docs', 'file.txt')

# 获取路径各部分
path = Path.home()
print(path)
print(path.parent)      # /home/user/docs
print(path.name)        # file.txt
print(path.stem)        # file（无后缀）
print(path.suffix)      # .txt
print(path.suffixes)    # ['.txt'] 或 ['.tar', '.gz']
print(path.anchor)      # 根部分，如 '/' 或 'C:\\'

# %%
path = Path('some_file.txt')

# 检查路径属性
path.exists()      # 是否存在
path.is_file()     # 是否是文件
path.is_dir()      # 是否是目录
path.is_absolute() # 是否是绝对路径

# 解析路径
path.resolve()     # 转为绝对路径（解析符号链接）
path.absolute()    # 转为绝对路径

# 相对路径计算
Path('/home/user').relative_to('/home')  # user
# %%
# 创建目录
path = Path().cwd()
path.mkdir(exist_ok=True)  # exist_ok=True 避免目录已存在时报错
path.mkdir(parents=True, exist_ok=True)  # 创建多级目录

# 删除
path.rmdir()  # 删除空目录
path.unlink(missing_ok=True)  # 删除文件，missing_ok=True 避免文件不存在时报错

# 重命名/移动
path.rename('new_name.txt')
path.replace('new_location.txt')  # 覆盖目标文件
# %%
path = Path('file.txt')

# 读写文本
text = path.read_text(encoding='utf-8')
path.write_text('Hello, world!', encoding='utf-8')

# 读写二进制
data = path.read_bytes()
path.write_bytes(b'Binary data')

# 使用 with 语句
with path.open('r', encoding='utf-8') as f:
    content = f.read()

# %%
path = Path().home()

# 遍历目录
for item in path.iterdir():
    print(item)  # 所有文件和子目录

# 递归遍历所有文件
# for file in path.rglob('*.py'):  # 递归查找.txt文件
#     print(file)

# for file in path.glob('**/*.txt'):  # 同上
#     print(file)

# 匹配子目录下的所有.txt文件
for file in path.glob('*/*.txt'):
    print(file)  # 当前目录下所有文件和目录

# 通配符查找
# list(path.glob('*.py'))      # 当前目录.py文件
# list(path.glob('docs/*.md')) # docs目录下.md文件
# %%    
path = Path('file.txt')

if path.exists():
    stat = path.stat()
    print(f"大小: {stat.st_size} bytes")
    print(f"修改时间: {stat.st_mtime}")
    print(f"创建时间: {stat.st_ctime}")
    
# 便捷属性
path.stat().st_size == path.stat().st_size  # 文件大小
# %%
