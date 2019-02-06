FROM python:3.6

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi pymysql psycopg2 cryptography
COPY . .
RUN pip install .
EXPOSE 8121
ENTRYPOINT [ "/bin/bash", "/usr/src/app/entrypoint.sh" ]
