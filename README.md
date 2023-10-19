# GrandetServer

## 构建 Docker 镜像

```bash
docker build -t grandet_server .
```

## 运行 Docker 容器

```bash
docker run --name grandet_container -p 8012:8000 -d grandet_server:latest
```
# 推送镜像到 Docker Hub

## 需要登陆docker

```bash
docker login
```

## 标记你的镜像

```bash
docker tag my_fastapi_app liupeng0/grandet_server:1.0.0
```

## 推送镜像到 Docker Hub

```bash
docker push liupeng0/grandet_server:1.0.0
```

