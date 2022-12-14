FROM python:3.8-slim-bullseye

COPY . /app
WORKDIR /app

ARG SECRET_KEY
ARG ALGORITHM
ARG MONGODB_URL_KEY
ARG DATABASE_NAME
ARG USER_COLLECTION_NAME
ARG EMBEDDING_COLLECTION_NAME

ENV SECRET_KEY=$SECRET_KEY
ENV ALGORITHM=$ALGORITHM
ENV MONGODB_URL_KEY=$MONGODB_URL_KEY
ENV DATABASE_NAME=$DATABASE_NAME
ENV USER_COLLECTION_NAME=$USER_COLLECTION_NAME
ENV EMBEDDING_COLLECTION_NAME=$EMBEDDING_COLLECTION_NAME

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && pip install -r requirements.txt

CMD ["python", "app.py"]