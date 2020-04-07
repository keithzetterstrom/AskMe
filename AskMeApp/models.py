from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class QuestionManager(models.Manager):
    def get_new_questions(self):
        new_questions = self.get_queryset().all().order_by('-make_time')
        return new_questions

    def get_questions_by_tag(self, tag):
        questions_by_tag = self.objects.filter(tags=tag)
        return questions_by_tag


class User(AbstractUser):
     avatar = models.ImageField(upload_to='avatars', default='avatars/avatar.jpeg')


class Tag(models.Model):
    tag_name = models.CharField(max_length=70, verbose_name=u"Название тэга")

    def __str__(self):
        return self.tag_name


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Заголовок вопроса")
    question_text = models.TextField(verbose_name=u"Текст вопроса")
    make_time = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE) #удалить объект, если удален объект автора
    tags = models.ManyToManyField(Tag, blank=True)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    answer_text = models.TextField(verbose_name=u"Текст ответа")
    make_time = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE) #удалить объект, если удален объект автора
    correct_mark = models.BooleanField()




