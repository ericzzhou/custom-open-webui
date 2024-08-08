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