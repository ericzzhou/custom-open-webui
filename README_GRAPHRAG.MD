## 官方主页
https://microsoft.github.io/graphrag/

## 初始化目录

- 安装 GraphRAG python 库
    ```bash
    pip install graphrag
    ```
- 在根目录创建文件夹 input 用来放置待处理的知识库源文件
- 在根目录创建文件夹 inputs 用来存储经过 GraphRAG 处理过的知识库文件
- 初始化 GraphRAG 工作空间
    ```bash
    python -m graphrag.index --init --root .
    ```

    此时会生成 .env 和 setting.yaml 文件 、prompt
    
    
    ### 修改 .env 

    ```bash
    GRAPHRAG_API_KEY=sk-XXXXXXX
    GRAPHRAG_ENTITY_EXTRACTION_PROMPT_FILE=prompts/entity_extraction.txt
    GRAPHRAG_COMMUNITY_REPORT_PROMPT_FILE=prompts/community_report.txt
    GRAPHRAG_SUMMARIZE_DESCRIPTIONS_PROMPT_FILE=prompts/summarize_descriptions.txt
    GRAPHRAG_LLM_MODEL=gpt-4o-mini
    # GRAPHRAG_EMBEDDING_MODEL=text-embedding-ada-002
    GRAPHRAG_EMBEDDING_MODEL=text-embedding-3-small
    ```

    ### 修改 setting.yaml
    ```yaml
    llm:
        type: openai_chat # or azure_openai_chat
        model: gpt-4o-mini
        # api_base: http://xxxx # 如果使用自建LLM ，需要在这里修改地址
        
    storage:
        base_dir: "inputs/artifacts"
    
    reporting:
        base_dir: "inputs/reports"
    
    claim_extraction: # 开启协变量
        enabled: true
        max_gleanings: 1
    ```

    ### 配置：开启协变量


## 创建 GraphRAG 索引

在根目录执行以下代码：
```bash
python -m graphrag.index --root .
```

## 提示词调优
```bash
python -m graphrag.prompt_tune --root . --no-entity-types
```
命令执行完成后，根目录会生成 prompts 目录。

在linux 或 类 linux 系统需要继续执行命令导入环境变量,windows 在 env 文件配置

```bash
export GRAPHRAG_ENTITY_EXTRACTION_PROMPT_FILE="prompts/entity_extraction.txt"
export GRAPHRAG_COMMUNITY_REPORT_PROMPT_FILE="prompts/community_report.txt"
export GRAPHRAG_SUMMARIZE_DESCRIPTIONS_PROMPT_FILE="prompts/summarize_descriptions.txt"
```