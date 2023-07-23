# версия питона
FROM python:3.10

# Рабочая директория для приложения в контейнере
WORKDIR /app

# Копируем файлы бота в рабочую директорию
COPY . /app
# чтобы исправить баг с импортом зависимостей
RUN apt-get update
# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "bot.py"]