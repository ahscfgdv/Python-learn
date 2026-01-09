# 安装：pip install opencc-python-reimplemented
import opencc


def traditional_to_simple_opencc(text):
    """
    使用 opencc 进行繁体转简体
    """
    converter = opencc.OpenCC('t2s')  # t2s: Traditional Chinese to Simplified Chinese
    return converter.convert(text)


# 使用示例
traditional_text = "這是一個繁體字的例子，歡迎使用Python腳本。"
simple_text = traditional_to_simple_opencc(traditional_text)
print(f"繁体: {traditional_text}")
print(f"简体: {simple_text}")


# 批量处理文件
def convert_file_opencc(input_file, output_file):
    converter = opencc.OpenCC('t2s')

    with open(input_file, 'r', encoding='utf-8') as f:
        traditional_content = f.read()

    simplified_content = converter.convert(traditional_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(simplified_content)

    print(f"文件转换完成: {input_file} -> {output_file}")