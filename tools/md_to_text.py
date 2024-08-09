import os
import markdown
from bs4 import BeautifulSoup

def convert_md_to_txt(md_file_path, output_dir):
    # 读取 Markdown 文件
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    
    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(md_content)
    
    # 将 HTML 转换为纯文本
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()

    # 生成输出的 TXT 文件路径
    relative_path = os.path.relpath(md_file_path, start=input_dir)
    txt_file_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + '.txt')

    # 确保输出目录存在
    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)

    # 将纯文本写入 TXT 文件
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)
    
    print(f"Converted: {md_file_path} to {txt_file_path}")

def convert_markdown_in_directory(input_dir):
    output_dir = os.path.join(os.getcwd(), '.data')
    
    # 遍历目录及其子目录
    for dirpath, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                md_file_path = os.path.join(dirpath, filename)
                convert_md_to_txt(md_file_path, output_dir)

if __name__ == "__main__":
    # 指定要查找的目录
    input_dir = input("请输入要查找的目录路径: ")
    
    if os.path.isdir(input_dir):
        convert_markdown_in_directory(input_dir)
        print("所有 Markdown 文件已成功转换为 TXT 文件。")
    else:
        print("输入的目录路径无效，请提供一个有效的目录。")