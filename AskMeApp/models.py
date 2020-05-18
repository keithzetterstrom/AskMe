from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Sum


class QuestionManager(models.Manager):
    def get_new_questions(self):
        # new_questions = self.get_queryset().all().order_by('-make_time'). \
        #     annotate(num_answer=Count('answer'), rating=Sum('likes_question__vote'))
        new_questions = self.get_queryset().all().order_by('-make_time'). \
            annotate(num_answer=Count('answer'))
        return new_questions

    def get_questions_by_tag(self, tag):
        questions_by_tag = self.get_queryset().order_by('-make_time') \
            .filter(tags__tag_name=tag).annotate(num_answer=Count('answer'))
        return questions_by_tag

    def get_questions_by_rating(self):
        questions_by_tag = self.get_queryset().order_by('-rating').annotate(num_answer=Count('answer', distinct=True))
        return questions_by_tag

    def get_question_by_id(self, question_id):
        question_by_id = self.get_queryset().get(id=question_id)
        return question_by_id

    def get_new_answers(self, question_obj):
        new_answers = question_obj.answer_set.all().order_by('-make_time')
        return new_answers


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to='avatars', default='avatar.jpeg')
    USERNAME_FIELD = 'username'


class Tag(models.Model):
    tag_name = models.CharField(max_length=70, verbose_name=u"Название тэга")

    def __str__(self):
        return f'Tag(pk={self.pk}):{self.tag_name}'


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1

    vote = models.SmallIntegerField(choices=range(LIKE, DISLIKE))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Заголовок вопроса")
    question_text = models.TextField(verbose_name=u"Текст вопроса")
    make_time = models.DateTimeField(auto_now_add=True, verbose_name=u"Время создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # удалить объект, если удален объект автора
    tags = models.ManyToManyField(Tag, blank=True)
    likes = GenericRelation(Like)
    rating = models.IntegerField(default=0, null=False, verbose_name='Рейтинг')
    answers_count = models.IntegerField(default=0, null=False, verbose_name='Количество ответов')
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
    rating = models.IntegerField(default=0, null=False, verbose_name='Рейтинг')

    def __str__(self):
        return f'Answer(pk={self.pk})'
