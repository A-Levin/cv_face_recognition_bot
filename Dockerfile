# версия питона
FROM python:3.10

# Рабочая директория для приложения в контейнере
WORKDIR /app

# Копируем файлы бота в рабочую директорию
COPY . /app

# чтобы исправить баг с импортом зависимостей
RUN apt update && apt install libgl1 -y
RUN ldconfig
# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Запускаем бота
CMD ["python", "bot.py"]
