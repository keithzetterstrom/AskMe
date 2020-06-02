from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Count


class QuestionManager(models.Manager):
    def get_new_questions(self):
        new_questions = self.all().prefetch_related('author').order_by('-make_time').\
            annotate(answers_count=Count('answer'))
        return new_questions

    def get_questions_by_tag(self, tag):
        questions_by_tag = self.all().prefetch_related('author').order_by('-make_time').\
            annotate(answers_count=Count('answer')).filter(tags__tag_name=tag)
        return questions_by_tag

    @property
    def get_questions_by_rating(self):
        questions_by_rating = self.prefetch_related('author').\
            annotate(answers_count=Count('answer')).\
            order_by('-rating')
        return questions_by_rating

    def get_question_by_id(self, question_id):
        question_by_id = self.get_queryset().get(id=question_id)
        return question_by_id

    def get_new_answers(self, question_obj):
        new_answers = question_obj.answer_set.all().order_by('-make_time')
        return new_answers


class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, question_id):
        answers = self.get_queryset().filter(question=Question(question_id))
        return answers

    def get_correct_answer(self, question_id):
        answer = self.get_queryset().filter(question=Question(question_id), correct_mark=True)
        return answer


class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to='avatars', default='avatar.jpeg')
    USERNAME_FIELD = 'username'


class Tag(models.Model):
    tag_name = models.CharField(max_length=70, unique=True, verbose_name=u"Название тэга", db_index=True)

    def __str__(self):
        return f'{self.tag_name}'


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1

    vote = models.SmallIntegerField(choices=range(LIKE, DISLIKE))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Заголовок вопроса")
    question_text = models.TextField(verbose_name=u"Текст вопроса")
    make_time = models.DateTimeField(auto_now_add=True, verbose_name=u"Время создания", db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # удалить объект, если удален объект автора
    tags = models.ManyToManyField(Tag, blank=True)
    likes = GenericRelation(Like)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг', db_index=True)
    #answers_count = models.IntegerField(default=0, null=False, verbose_name='Количество ответов')
    objects = QuestionManager()

    def __str__(self):
        return f'Question(pk={self.pk}):{self.title}'


class Answer(models.Model):
    answer_text = models.TextField(verbose_name=u"Текст ответа")
    make_time = models.DateTimeField(auto_now_add=True, verbose_name=u"Время создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # удалить объект, если удален объект автора
    correct_mark = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = GenericRelation(Like)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    objects = AnswerManager()

    def __str__(self):
        return f'Answer(pk={self.pk})'
