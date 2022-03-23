from django.core.validators import MinLengthValidator
from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
from django.urls import reverse


User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    content = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Контент")
    tags = models.ManyToManyField("webapp.Tag", related_name="articles")
    author = models.ForeignKey(
        User,
        related_name="articles",
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name="Автор",
    )
    likes = models.ManyToManyField(get_user_model(), through='webapp.ArticleLike', through_fields=('article', 'user'))

    def get_absolute_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.pk})

    def upper(self):
        return self.title.upper()

    def __str__(self):
        return f"{self.pk}. {self.author}: {self.title}"


    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Tag(BaseModel):
    name = models.CharField(max_length=30, verbose_name="Тег")

    def __str__(self):
        return f"{self.pk} - {self.name}"

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Comment(BaseModel):
    content = models.TextField(max_length=2000, verbose_name="Контент")
    author = models.ForeignKey(
        User,
        related_name="comments",
        default=1,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    article = models.ForeignKey("webapp.Article", on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name="Статья",
                                )
    likes = models.ManyToManyField(get_user_model(), through='webapp.CommentLike', through_fields=('comment', 'user'))

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class ArticleLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='article_likes', verbose_name='Пользователь')
    article = models.ForeignKey('webapp.Article', on_delete=models.CASCADE,
                                related_name='articles_likes', verbose_name='Статья')

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки статей'


class CommentLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='comment_likes', verbose_name='Пользователь')
    comment = models.ForeignKey('webapp.Comment', on_delete=models.CASCADE,
                                related_name='comment_likes', verbose_name='Комментарий')

    def __str__(self):
        return f'{self.user.username} - {self.comment.author}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки комментариев'
