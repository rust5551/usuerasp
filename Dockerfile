FROM python:3.10.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 80/tcp

CMD [ "python", "bot.py", "runserver", "0.0.0.0:8000" ]