import datetime

from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    if value == 'me':
        raise ValidationError('Имя пользователя "me" нельзя.')


def validate_year(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            f'Год не может быть больше текущего ({current_year}).'
        )
