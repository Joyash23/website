FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk add sqlite

COPY . .

CMD [ "quickweb", "run", "/usr/src/app" ]
