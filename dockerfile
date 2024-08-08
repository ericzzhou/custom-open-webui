# 使用 Python 3.12-slim 作为基础镜像
FROM python:3.12-slim AS builder

# 更新包列表并安装 poppler-utils 和依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt /app/

# 安装 Python 依赖
RUN pip3 install --no-cache-dir -r requirements.txt

###################################################################### 
# 使用一个更小的镜像作为运行时镜像
FROM python:3.12-slim    

# 更新包列表并安装 poppler-utils
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app
# 复制已安装的依赖
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app/

# 暴露端口
EXPOSE 8765

ENV GRAPHRAG_API_KEY=sk-XXXX
ENV GRAPHRAG_ENTITY_EXTRACTION_PROMPT_FILE=prompts/entity_extraction.txt
ENV GRAPHRAG_COMMUNITY_REPORT_PROMPT_FILE=prompts/community_report.txt
ENV GRAPHRAG_SUMMARIZE_DESCRIPTIONS_PROMPT_FILE=prompts/summarize_descriptions.txt
ENV GRAPHRAG_LLM_MODEL=gpt-4o-mini
# GRAPHRAG_EMBEDDING_MODEL=text-embedding-ada-002
ENV GRAPHRAG_EMBEDDING_MODEL=text-embedding-3-small

# 定义数据卷
VOLUME ["/app/inputs","/app/input"]

# 设置容器启动时运行的命令
CMD ["python3", "app.py"]
