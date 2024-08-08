# custom-open-webui
围绕open-webui 周边的一系列工具集成

# build 镜像
docker build 时忽略 inputs 文件，此文件应该映射到主机目录

```
sudo docker build --pull --rm -f "dockerfile" -t custom-open-webui:latest "." 
```

# 启动
```
sudo docker run -d -p 8765:8765 -v /home/openai/src/knowledge-base-catalog/inputs:/app/inputs -v /home/openai/src/knowledge-base-catalog/input:/app/input --name custom-open-webui custom-open-webui 
```


注意： 修改 dockerfile 里的 GRAPHRAG_API_KEY（open_api_key） 和 GRAPHRAG_LLM_MODEL (模型)

# 配置
docker 运行时候，需要加载 .env 文件 到 Docker Env 环境变量

或者在 docker 启动的时候使用 -e GRAPHRAG_API_KEY=your_api_key_here 设置

```

GRAPHRAG_API_KEY=sk-xxxx
GRAPHRAG_ENTITY_EXTRACTION_PROMPT_FILE="prompts/entity_extraction.txt"
GRAPHRAG_COMMUNITY_REPORT_PROMPT_FILE="prompts/community_report.txt"
GRAPHRAG_SUMMARIZE_DESCRIPTIONS_PROMPT_FILE="prompts/summarize_descriptions.txt"
GRAPHRAG_LLM_MODEL="gpt-4o-mini"
# GRAPHRAG_EMBEDDING_MODEL="text-embedding-ada-002"
GRAPHRAG_EMBEDDING_MODEL="text-embedding-3-small"
```