from django.core.management.base import BaseCommand
from django.db.models import Sum
from AskMeApp.models import User


class Command(BaseCommand):
    help = 'users_rating'

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
            user.rating = user_rating
            user.save()

    def handle(self, *args, **options):
        self.rating_user()
