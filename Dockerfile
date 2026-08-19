# ベースイメージをDebianベースのPythonイメージに変更
FROM public.ecr.aws/docker/library/python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y  \
    vim \
    less \
    curl \
    zip \
    unzip && \
    apt-get clean && \
    apt-get autoclean

RUN apt-get update && apt-get -y install nginx logrotate tzdata && apt-get clean

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod -R 755 /etc/nginx

COPY docker/nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/config/mime.types /etc/nginx/mime.types
COPY docker/nginx/config/fastcgi_params /etc/nginx/fastcgi_params

RUN chmod +x /app/scripts/start-uvicorn.sh

ENV PYTHONPATH=/app/app

EXPOSE 80

ENTRYPOINT ["/app/scripts/start-uvicorn.sh"]

CMD ["true"]
