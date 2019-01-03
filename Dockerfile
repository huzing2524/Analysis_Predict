FROM python:3.6

# PostgreSQL setting
ENV PG_DATABASE="db_dsd" \
    PG_USER="dsdUser" \
    PG_PASSWORD="dsdUserPassword" \
    PG_HOST="postgres" \
    PG_PORT="5432"

RUN mkdir -p /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 
