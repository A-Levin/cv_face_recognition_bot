import logging
import os
from aiogram import Bot, Dispatcher, executor, types

from face_recognition import extract_faces_from_directory

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", 'Insert your token here')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет! Я бот который извлекает лица с фоток и возвращает их в"
                        " разрешении 100х100.\n1. Просто отправь мне фотки. \n2. Вызови"
                        " команду /extract_faces \n3. Получи извлеченные лица")

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def handle_photo_or_document(message: types.Message):
    """
    This handler will put all photos in a directory called 'sources'
    :param message:
    :return:
    """
    # Проверяем, что директория 'sources' существует
    if not os.path.exists('sources'):
        os.makedirs('sources')

    # Получаем объект File, который хранит информацию о файле и его загрузке
    photo = message.photo[-1]

    # Скачиваем файл в директорию 'sources'
    await photo.download('sources/' + photo.file_id + '.jpg')

    # Отправляем пользователю сообщение об успешной загрузке
    await message.reply("Photo saved successfully")

@dp.message_handler(commands=['extract_faces'])
async def extract_faces(message: types.Message):
    """
    This handler will extract faces from all photos in the 'sources' directory
    :param message:
    :return:
    """
    # Проверяем, что директория 'sources' существует
    if not os.path.exists('sources'):
        await message.reply("Directory 'sources' does not exist")
        return

    # Проверяем, что директория 'faces' существует
    if not os.path.exists('faces'):
        os.makedirs('faces')

    # Извлекаем лица из всех фотографий в директории 'sources'
    extract_faces_from_directory('sources', 'faces')

    # Отправляем пользователю сообщение об успешном извлечении лиц
    await message.reply("Faces extracted successfully")

    # Отправляем пользователю все извлеченные лица
    for filename in os.listdir('faces'):
        with open('faces/' + filename, 'rb') as photo:
            await message.reply_photo(photo)
    # Очищаем директории 'sources' и 'faces'
    for filename in os.listdir('sources'):
        os.remove('sources/' + filename)
    for filename in os.listdir('faces'):
        os.remove('faces/' + filename)

    # Отправляем пользователю сообщение, что фотки удалены
    await message.reply("Photos deleted successfully")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)