import random
from django.core.management.base import BaseCommand
from faker import Faker
from AskMeApp.models import Question, User, Answer, Tag

f = Faker()
# tags_lst = ['Python', 'SQl', 'C++', 'Django', 'PyCharm', 'C',
#             'C#', 'JavaScript', 'Java', 'HTML', 'CSS', 'MySQL',
#             'wsgi', 'GO', 'Docker', 'nginx', 'Linux', 'email',
#             'MySQL', 'database', 'Shadow']


class Command(BaseCommand):
    help = 'filldb'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true')
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--answers', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
            #User.objects.create(username=f.name())
            User.objects.create(username=i)

    def fill_questions(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))

        for i in range(cnt):
            vote = random.choice(range(-30, 50))
            Question.objects.create(
                author_id=random.choice(author_ids),
                question_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:200],
                rating=vote,
            )

    def fill_tags(self, cnt):
        questions_ids = list(Question.objects.values_list('id', flat=True))
        #tags_lst = f.words(cnt)
        for i in range(0, cnt):
            try:
                t = Tag(tag_name=i)
                t.save()
                for j in random.sample(questions_ids, random.choice(range(1, 5))):
                    t.question_set.add(j)
            except:
                pass

    def fill_answers(self, cnt):
        author_ids = list(User.objects.values_list('id', flat=True))
        questions_ids = list(Question.objects.values_list('id', flat=True))

        for i in range(cnt):
            votes = random.choice(range(-30, 50))
            Answer.objects.create(
                author_id=random.choice(author_ids),
                answer_text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                question_id=random.choice(questions_ids),
                rating=votes,
            )

    def fill_db(self):
        self.fill_authors(10000)
        print('authors done')
        self.fill_questions(100000)
        print('questions done')
        self.fill_tags(10000)
        print('tags done')
        self.fill_answers(1000000)
        print('answers done')

    def handle(self, *args, **options):
        authors = options['authors']
        questions = options['questions']
        tags = options['tags']
        answers = options['answers']
        if options['all']:
            self.fill_db()
        if authors:
            self.fill_authors(authors)
        if questions:
            self.fill_questions(questions)
        if tags:
            self.fill_tags(tags)
        if answers:
            self.fill_answers(answers)
