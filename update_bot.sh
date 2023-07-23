#!/bin/bash

# Остановить текущий контейнер cv_recognition_bot
docker stop cv_recognition_bot

# Удалить старый контейнер cv_recognition_bot
docker rm cv_recognition_bot

# Собрать новый Docker образ с помощью Dockerfile
docker build -t cv_recognition_bot .

# Запустить новый контейнер cv_recognition_bot с обновленным образом
docker run --restart=always -d -p 3000:3000 --name cv_recognition_bot --env-file .env cv_recognition_bot
