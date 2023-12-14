FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Копируем зависимости
COPY ./ /app
COPY ./requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install  -r /app/requirements.txt
