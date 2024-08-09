# 脚本的工作原理是：

# 使用pandas库读取Excel文件。

# 将数据框格式化为Markdown字符串和普通文本字符串。

# 将这些字符串分别保存为.md文件和.txt文件。


# 可以修改 excel_to_md_and_txt("your_excel_file.xlsx", sheet_name=0) 这一行代码，将 "your_excel_file.xlsx" 替换为你实际的Excel文件名。
# 如果您的文件有多个表，可以通过更改 sheet_name 参数来选择特定的表。


import os


class Excel2XXX:
    def __init__(self, excel_file, sheet_name=0):
        self.excel_file = excel_file
        self.sheet_name = sheet_name

    def getFilepath(self):
        # 获取当前执行文件的目录
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # 计算文件的绝对路径
        excelFile = os.path.abspath(os.path.join(script_directory, self.excel_file))
        # txt = os.path.abspath(os.path.join(script_directory, self.txt_path))
        return excelFile

    def read_excel(self):
        import pandas as pd

        self.excel_file = self.getFilepath()
        # 读取Excel文件
        df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
        return df

    def to_txt(self):
        df = self.read_excel()
        # 转换为文本格式
        txt_content = df.to_string(index=False)
        # 保存为.txt文件
        txt_file = self.excel_file.replace(".xlsx", ".txt").replace(".xls", ".txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(txt_content)

        print(f"文本文件保存为: {txt_file}")

    def to_markdown(self):
        df = self.read_excel()

        # 转换为Markdown格式
        md_content = df.to_markdown(index=False)

        # 保存为.md文件
        md_file = self.excel_file.replace(".xlsx", ".md").replace(".xls", ".md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Markdown文件保存为: {md_file}")

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"目录 '{directory}' 已创建。")
        else:
            print(f"目录 '{directory}' 已存在。")


if __name__ == "__main__":
    # 设置 PDF 文件路径和输出的 TXT 文件路径
    file = "assets/CS 语料.xlsx"

    # # 调用函数
    excel = Excel2XXX(file)
    excel.to_markdown()
    excel.to_txt()
