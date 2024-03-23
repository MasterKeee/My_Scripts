# Created by MasterKe on 2023/11/8.
import re
# 提示用户输入文本文件路径
file_path = input("请输入文案的路径：")

# 读取文本文件
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 删除指定符号以外的所有标点符号，保留前面符号是为了换行
text = re.sub(r'[^,，。？！：；\u4e00-\u9fa5a-zA-Z0-9\u002d“”"《》~°、.（）()\n]', '', text)

# 将每一句话放在一行
text = re.sub(r'[,，。？！：；]', '\n', text)
# 删除多余的换行符
text = re.sub(r'\n+', '\n', text)

# 将处理好的文字替换原来的文本
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(text)
input("按回车退出···")