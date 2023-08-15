FROM python:3.10.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# specifying the working directory inside the container
WORKDIR /usr/src/app

RUN apt update \
    && apt install -y gcc libgeos-dev git netcat \
    && pip install --upgrade pip \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

# installing the Python dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copying the contents of our app' inside the container

COPY . .

# running Flask as a module, we sleep a little here to make sure that the DB is fully instanciated before running our app'
CMD ["sh", "-c", "sleep 5 && python -m flask --debug run --host=0.0.0.0"]