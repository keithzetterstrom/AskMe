from django.core.management.base import BaseCommand
from AskMeApp.models import Question, User, Answer, Tag, Like
from random import choice, random, randint
from faker import Faker

f = Faker()
tags_lst = ['Python', 'SQl', 'C++', 'Django', 'PyCharm', 'C', 'C#', 'JavaScript', 'Java', 'HTML', 'CSS', 'MySQL']


class Command(BaseCommand):
    help = 'filldb'

    def add_arguments(self, parser):
        parser.add_argument('--tags',  action='store_true')
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)

    def fill_tags(self):
        for t in tags_lst:
            Tag.objects.create(tag_name=t)

    def fill_authors(self, cnt):
        for i in range(cnt):
            u = User(username=f.name())
            u.save()

    def fill_questions(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        for i in range(cnt):
            q = Question(
                author=User(choice(author_ids)),
                question_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:200],
            )
            q.save()

            for i in range(randint(0, 6)):
                tag = choice(tag_ids)
                if tag not in q.tags.values_list('id'):
                    q.tags.add(tag)

    def fill_answers(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))
        questions_ids = list(Question.objects.values_list('id', flat=True))

        for i in range(cnt):
            a = Answer(
                author=User(choice(author_ids)),
                answer_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                question=Question(choice(questions_ids)),
            )
            a.save()

    def fill_likes(self):
        author_ids = list(User.objects.values_list('id', flat=True))
        questions_ids = list(Question.objects.values_list('id', flat=True))
        answers_ids = list(Answer.objects.values_list('id', flat=True))
        vote = (1, -1)

        for question in questions_ids:
            for i in range(randint(0, 30)):
                l = Like(
                    user=User(choice(author_ids)),
                    vote=choice(vote),
                    object_id=question
                )
                l.save()

        for answer in answers_ids:
            for i in range(randint(0, 20)):
                a = Like(
                    user=User(choice(author_ids)),
                    vote=choice(vote),
                    object_id=answer
                )
                a.save()

    def handle(self, *args, **options):
        authors = options['authors']
        questions = options['questions']
        answers = options['answers']
        if options['tags']:
            self.fill_tags()
        if authors:
            self.fill_authors(authors)
        if questions:
            self.fill_questions(questions)
        if answers:
            self.fill_answers(answers)

