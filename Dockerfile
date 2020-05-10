FROM python:3.8

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir uwsgi pymysql psycopg2 cryptography
EXPOSE 8121
ENTRYPOINT [ "/bin/bash", "/usr/src/app/entrypoint.sh" ]
