# Generated by Django 3.0.4 on 2020-06-02 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AskMeApp', '0010_auto_20200601_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(db_index=True, max_length=70, unique=True, verbose_name='Название тэга'),
        ),
    ]
