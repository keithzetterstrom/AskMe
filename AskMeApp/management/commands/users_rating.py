from django.core.management.base import BaseCommand
from django.db.models import Sum
from AskMeApp.models import User
from django.core.cache import cache


class Command(BaseCommand):
    help = 'users_rating'
    dct = {}

    def rating_user(self):
        users_objs = User.objects.all()
        for user in users_objs:
            questions_rating = user.question_set.all().aggregate(questions_rating=Sum('rating'))
            answers_rating = user.answer_set.all().aggregate(answers_rating=Sum('rating'))
            user_rating = 0
            try:
                user_rating += questions_rating['questions_rating']
            except:
                pass
            try:
                user_rating += answers_rating['answers_rating']
            except:
                pass
            self.dct.update({user.username: user_rating})

    def rating_sort(self):
        lst_d = list(self.dct.items())
        lst_d.sort(key=lambda i: i[1])
        lst_d.reverse()
        lst_names = []
        for i in lst_d:
            lst_names.append(i[0])
        cache.set('top100_users', lst_names, 1800)

    def handle(self, *args, **options):
        self.rating_user()
        self.rating_sort()
