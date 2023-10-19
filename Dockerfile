# 使用官方 Python 基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /usr/src/grandet/app

# 将当前目录的内容复制到工作目录中
COPY ./app .
COPY ./requirements.txt /usr/src/grandet/app/requirements.txt


# 安装项目依赖
# RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple -U pip 
# RUN pip3 config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install --no-cache-dir -r requirements.txt 

# 暴露你的应用程序端口
EXPOSE 8000

# 定义启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
