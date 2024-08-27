FROM python:3.10.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 443/tcp

CMD ["python", "bot.py"]