import os
import cv2

def extract_faces_from_directory(input_directory, output_directory, scale_factor=1.3, min_neighbors=5, target_size=(200, 200)):
    # Загрузка классификатора Haar Cascade для обнаружения лиц
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Создание выходной директории, если она не существует
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Перебор всех файлов в директории
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_directory, filename)
            output_image_path = os.path.join(output_directory, filename)

            # Загрузка изображения
            image = cv2.imread(input_image_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Обнаружение лиц на изображении с использованием Haar Cascade
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=scale_factor, minNeighbors=min_neighbors)

            # Вырезаем обнаруженные лица и сохраняем их в отдельные файлы
            for i, (x, y, w, h) in enumerate(faces):
                face = image[y:y+h, x:x+w]

                # Ресайз лица до 200x200 пикселей
                if target_size:
                    face = cv2.resize(face, target_size)

                # Сохраняем лицо в выходную директорию
                output_filename = f"{os.path.splitext(filename)[0]}_face_{i}.jpg"
                output_image_path = os.path.join(output_directory, output_filename)
                cv2.imwrite(output_image_path, face)

