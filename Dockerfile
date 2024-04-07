FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x run.sh
CMD ["./run.sh"]
