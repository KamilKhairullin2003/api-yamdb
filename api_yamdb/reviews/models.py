from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.const import (
    MAIL_LENGTH, NAME_LENGTH,
    MIN, MAX, TEXT_MAX, USERNAME_LENGTH
)
from reviews.validators import validate_username_not_me, validate_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Аутенфицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=[AbstractUser.username_validator, validate_username_not_me]
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=MAIL_LENGTH
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь админом или суперюзером."""

        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""

        return self.role == self.MODERATOR


User = get_user_model()


class CategoryGenreBase(models.Model):
    name = models.CharField(verbose_name='Название', max_length=NAME_LENGTH)
    slug = models.SlugField(verbose_name='Идентификатор', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class ReviewCommentBase(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_MAX]


class Category(CategoryGenreBase):
    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=NAME_LENGTH)
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN), MaxValueValidator(MAX)]
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
