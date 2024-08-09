# custom-open-webui
围绕open-webui 周边的一系列工具集成

- [GraphRAG 环境初始化](./README_GRAPHRAG.MD)

# 运行

## 第一步：配置
docker 运行时候，需要加载 .env 文件 到 Docker Env 环境变量

或者在 docker 启动的时候使用 -e GRAPHRAG_API_KEY=your_api_key_here 设置

```bash

GRAPHRAG_API_KEY=sk-xxxx # LLM ApiKey
GRAPHRAG_ENTITY_EXTRACTION_PROMPT_FILE=prompts/entity_extraction.txt
GRAPHRAG_COMMUNITY_REPORT_PROMPT_FILE=prompts/community_report.txt
GRAPHRAG_SUMMARIZE_DESCRIPTIONS_PROMPT_FILE=prompts/summarize_descriptions.txt
GRAPHRAG_LLM_MODEL=gpt-4o-mini 
# GRAPHRAG_EMBEDDING_MODEL=text-embedding-ada-002
GRAPHRAG_EMBEDDING_MODEL=text-embedding-3-small
```

## 第二步：build 镜像
docker build 时忽略 inputs 和 input 文件，此文件应该映射到主机目录

```bash
sudo docker build --pull --rm -f "dockerfile" -t custom-open-webui:latest "." 
```

## 第三步：启动
```bash
sudo docker run -d -p 8765:8765 -v /home/openai/src/knowledge-base-catalog/inputs:/app/inputs -v /home/openai/src/knowledge-base-catalog/input:/app/input --name custom-open-webui custom-open-webui 
```


注意： 使用 -e 添加环境变量： GRAPHRAG_API_KEY（open_api_key） 和 GRAPHRAG_LLM_MODEL (模型) 或在 dockerfile 内修改

## 第四步：上传知识库文件【仅支持.txt】

```bash
# 上传 GraphRag 整理好的知识库文件到以下宿主机目录 /home/openai/src/knowledge-base-catalog/inputs:/app/inputs
```

## 映射端口并访问
```bash
[GET] http://127.0.0.1:8765/v1/models # 列出所有可用模型
[POST] http://localhost:8765/v1/chat/completions # 向模型提问
```

### 提问示例
```bash
curl --location 'http://localhost:8765/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
    "model": "rag:graph_rag_demo",
    "messages": [
      {
        "role": "system",
        "content": "你是一个友好的AI助手"
      },
      {
        "role": "user",
        "content": "范闲的兄弟是谁"
      },
      {
        "role": "assistant",
        "content": "上次的搜索结果"
      },
      {
        "role": "user",
        "content": "范闲的敌人都有谁"
      }
    ]
  }'
```