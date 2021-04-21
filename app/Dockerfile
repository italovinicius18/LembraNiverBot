FROM python:3.7

WORKDIR /usr/src/app

RUN cd app/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "handleBot.py" ]
