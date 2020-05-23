import random
from django.core.management.base import BaseCommand
from faker import Faker
from AskMeApp.models import Question, User, Answer, Tag, Like

f = Faker()
tags_lst = ['Python', 'SQl', 'C++', 'Django', 'PyCharm', 'C', 'C#', 'JavaScript', 'Java', 'HTML', 'CSS', 'MySQL']


class Command(BaseCommand):
    help = 'filldb'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true')
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
            #u = User(username=i)
            u.save()

    def fill_questions(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))
        vote = (1, -1)

        for i in range(cnt):
            q = Question(
                author_id=random.choice(author_ids),
                question_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:200],
            )
            q.save()

            for i in range(random.randint(0, 40)):
                v = random.choice(vote)
                q.likes.create(user=User(author_ids[i]), vote=v)
                if v > 0:
                    q.likes_count += 1
                else:
                    q.dislikes_count += 1
                q.save()

            for i in range(random.randint(0, 6)):
                tag = random.choice(tag_ids)
                if tag not in q.tags.values_list('id'):
                    q.tags.add(tag)

    def fill_answers(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))
        questions_ids = list(Question.objects.values_list('id', flat=True))
        vote = (1, -1)

        for i in range(cnt):
            questions_obj = Question.objects.get(pk=random.choice(questions_ids))
            a = Answer(
                author=User(random.choice(author_ids)),
                answer_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                question=questions_obj,
            )
            a.save()
            questions_obj.answers_count += 1
            questions_obj.save()
            for i in range(random.randint(0, 40)):
                v = random.choice(vote)
                a.likes.create(user=User(author_ids[i]), vote=v)
                if v > 0:
                    a.likes_count += 1
                else:
                    a.dislikes_count += 1
                a.save()

    def fill_db(self):
        self.fill_tags()
        self.fill_authors(50)
        print('authors done')
        self.fill_questions(100)
        print('questions done')
        self.fill_answers(200)
        print('answers done')

    def handle(self, *args, **options):
        authors = options['authors']
        questions = options['questions']
        answers = options['answers']
        if options['all']:
            self.fill_db()
        if options['tags']:
            self.fill_tags()
        if authors:
            self.fill_authors(authors)
        if questions:
            self.fill_questions(questions)
        if answers:
            self.fill_answers(answers)
