FROM python:3.8.5

WORKDIR /app/telegram_bot
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt /app/telegram_bot
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "./app.py"]