FROM python:latest

ENV TZ Asia/Tokyo

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# CMD ["python", "/app/libs/line_bot.py"]
