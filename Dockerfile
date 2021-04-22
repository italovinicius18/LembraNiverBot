FROM python:3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r app/requirements.txt


CMD [ "python", "app/handleBot.py" ]
