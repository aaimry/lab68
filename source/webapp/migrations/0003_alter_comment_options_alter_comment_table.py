# Generated by Django 4.0 on 2022-01-10 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comments',
        ),
    ]