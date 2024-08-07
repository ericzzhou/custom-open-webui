# 使用 Python 3.12 作为基础镜像
FROM python:3.12

# 更新包列表并安装 poppler-utils
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

COPY . /app/
# 安装 Python 依赖（这部分可以不需要，因为依赖文件会在宿主机上）
# 这里如果需要，可以写在 RUN 指令中，具体视项目需求而定

# 安装 Python 依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8765

# 定义数据卷
VOLUME ["/app/inputs"]

# 设置容器启动时运行的命令
CMD ["python3", "app.py"]
