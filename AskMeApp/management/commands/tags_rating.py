from django.core.management.base import BaseCommand
from AskMeApp.models import Tag


class Command(BaseCommand):
    help = 'tags_rating'

    def rating_tags(self):
        tags_objs = Tag.objects.all()
        for tag in tags_objs:
            count = tag.question_set.all().count()
            tag.questions_count = count
            tag.save()

    def handle(self, *args, **options):
        self.rating_tags()
