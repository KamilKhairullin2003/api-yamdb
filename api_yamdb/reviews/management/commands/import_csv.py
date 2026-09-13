import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()

FIELD_MAP = {
    'author': 'author_id',
    'category': 'category_id',
}

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в базу данных'

    def handle(self, *args, **kwargs):
        csv_dir = os.path.join(settings.BASE_DIR, 'static', 'data')

        for model, file_name in TABLES.items():
            file_path = os.path.join(csv_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    mapped_row = {}
                    for key, value in row.items():
                        new_key = FIELD_MAP.get(key, key)
                        mapped_row[new_key] = value

                    model.objects.get_or_create(**mapped_row)
            self.stdout.write(
                self.style.SUCCESS(f'Успешно загружен {file_name}')
            )

        genre_title_path = os.path.join(csv_dir, 'genre_title.csv')
        with open(genre_title_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)

        self.stdout.write(
            self.style.SUCCESS('Связи жанров и произведений установлены')
        )
