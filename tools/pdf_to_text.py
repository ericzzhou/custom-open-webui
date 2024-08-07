import os


class Pdf2Text:
    def __init__(self, pdf_path, txt_path):
        self.pdf_path = pdf_path
        self.txt_path = txt_path

    def getFilepath(self):
        # 获取当前执行文件的目录
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # 计算文件的绝对路径
        pdf = os.path.abspath(os.path.join(script_directory, self.pdf_path))
        txt = os.path.abspath(os.path.join(script_directory, self.txt_path))

        self.pdf_fullpath = pdf
        self.txt_fullpath = txt
        return pdf, txt

    def usePyPDF2(self):
        import PyPDF2

        pdf, txt = self.getFilepath()
        # 打印文件路径用于调试
        print(f"正在尝试访问文件: {pdf}")
        try:
            if not os.path.exists(pdf):
                raise FileNotFoundError(f"文件不存在: {pdf}")
            # 打开 PDF 文件
            with open(pdf, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)

                self.fileTitle = reader.metadata.title

                # 创建或打开 TXT 文件
                with open(txt, "w", encoding="utf-8") as txt_file:
                    # 遍历每一页并提取文本
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        txt_file.write(text)
                        txt_file.write("\n")  # 换行符
            print(f"PDF 文件已成功转换为 {txt}")
        except Exception as e:
            print(f"转换过程中出现错误: {e}")

    def usePdfplumber(self):
        import pdfplumber

        pdf, txt = self.getFilepath()
        # 打印文件路径用于调试
        print(f"正在尝试访问文件: {pdf}")
        try:
            if not os.path.exists(pdf):
                raise FileNotFoundError(f"文件不存在: {pdf}")
            # 打开 PDF 文件
            with pdfplumber.open(pdf) as pdf_file:
                self.fileTitle = pdf_file.metadata.get("title", "未知标题")
                # 创建或打开 TXT 文件
                with open(txt, "w", encoding="utf-8") as txt_file:
                    for page in pdf_file.pages:
                        text = page.extract_text()
                        if text:
                            txt_file.write(text)
                            txt_file.write("\n")  # 添加换行符
            print(f"PDF 文件已成功转换为 {txt}")
        except Exception as e:
            print(f"转换过程中出现错误: {e}")

    def usePyMuPDF(self):
        import fitz

        pdf, txt = self.getFilepath()
        # 打印文件路径用于调试
        print(f"正在尝试访问文件: {pdf}")
        try:
            if not os.path.exists(pdf):
                raise FileNotFoundError(f"文件不存在: {pdf}")

            # 打开 PDF 文件
            pdf_document = fitz.open(pdf)
            self.fileTitle = pdf_document.metadata.get("title")
            # 创建或打开 TXT 文件
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                # 遍历每一页并提取文本
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    text = page.get_text()

                    if text:
                        txt_file.write(text)
                        txt_file.write("\n")  # 换行符
            print(f"PDF 文件已成功转换为 {txt_path}")
        except Exception as e:
            print(f"转换过程中出现错误: {e}")

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"目录 '{directory}' 已创建。")
        else:
            print(f"目录 '{directory}' 已存在。")

    def initGraphRAG(self):
        if (
            self.fileTitle is None
            or self.fileTitle == ""
            or not self.fileTitle
            or len(self.fileTitle) == 0
        ):
            print("文件名为空，无法创建知识库目录。")
            return

        # 获取当前执行文件的目录
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # 当前知识库的根目录
        knowledgeDic = os.path.abspath(
            os.path.join(script_directory, "..", "graphRAG", self.fileTitle, "input")
        )

        self.ensure_dir(knowledgeDic)

        # 将 txt 知识库源文件移动到目录
        import shutil

        # 移动后的最终txt文件
        self.final_knowledge_sourcefile = shutil.move(self.txt_fullpath, knowledgeDic)
        print(f"目标：{self.final_knowledge_sourcefile}")

        # 初始化知识库目录
        import subprocess

        # 执行一个简单的 shell 命令
        rootKnowledgeDic = os.path.abspath(os.path.join(knowledgeDic, ".."))

        print(
            f"执行命令初始化知识库: python -m graphrag.index --init --root {rootKnowledgeDic}"
        )
        result = subprocess.run(
            ["python", "-m", "graphrag.index", "--init", "--root", rootKnowledgeDic],
            capture_output=True,
            text=True,
        )
        print(f"命令输出：{result.stdout}")

        # TODO: 手动修改 .env 文件里的OpenAI Key
        # TODO: 手动修改 settings.yami 文件里的模型和模型地址
        # TODO: 手动 索引

        return ""


if __name__ == "__main__":
    # 设置 PDF 文件路径和输出的 TXT 文件路径
    pdf_path = "assets/面向所有人的机器学习科普大全.pdf"
    txt_path = "assets/面向所有人的机器学习科普大全.txt"

    # # 调用函数
    pdf = Pdf2Text(pdf_path, txt_path)
    pdf.usePyPDF2()
    pdf.initGraphRAG()
    print(f"处理的文件名：{pdf.fileTitle}")
