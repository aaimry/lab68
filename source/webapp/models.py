from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    author = models.CharField(max_length=200, null=False, blank=False, verbose_name="Автор", default="Unknown")
    content = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Контент")

    def __str__(self):
        return f"{self.pk}. {self.author}: {self.title}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(BaseModel):
    content = models.TextField(max_length=2000,verbose_name="Контент")
    author = models.CharField(max_length=200, null=True, blank=True, verbose_name="Автор", default="Аноним")
    article = models.ForeignKey("webapp.Article", on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name="Статья",
                               )

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'