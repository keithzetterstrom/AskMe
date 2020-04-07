from django.core.management.base import BaseCommand
from AskMeApp.models import Question, User
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):
    help = 'filldb'

    def add_arguments(self, parser):
        # parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        # parser.add_argument('--answers', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
            u = User(username=f.name())
            u.save()
            # Author.objects.create(
            #     rating=f.random_int(min=-100, max=100),
            #     user=u
            # )

    def fill_questions(self, cnt):
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Question.objects.create(
                author=User(choice(author_ids)),
                question_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:200],
            )

    def handle(self, *args, **options):
        # self.fill_authors(options.get('authors', 0))
        self.fill_questions(options.get('questions', 0))
        # self.fill_answers(answers_cnt)
