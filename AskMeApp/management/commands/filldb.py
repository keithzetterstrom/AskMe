from django.core.management.base import BaseCommand
from AskMeApp.models import Question, User, Answer
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):
    help = 'filldb'

    def add_arguments(self, parser):
        #parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        #parser.add_argument('--answers', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
            u = User(username=f.name())
            u.save()

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

    def fill_answers(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))

        questions_ids = list(Question.objects.values_list('id', flat=True))

        for i in range(cnt):
            Answer.objects.create(
                author=User(choice(author_ids)),
                answer_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:200],
                question=Question(choice(questions_ids))
            )

    def handle(self, *args, **options):
        #self.fill_authors(options.get('authors', 0))
        self.fill_questions(options.get('questions', 0))
        #self.fill_answers(options.get('questions', 0))
