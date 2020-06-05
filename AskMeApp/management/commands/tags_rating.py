from django.core.management.base import BaseCommand
from AskMeApp.models import Tag


class Command(BaseCommand):
    help = 'tags_rating'

    def rating_tags(self):
        tags_ids = list(Tag.objects.values_list('id', flat=True))
        for tag_id in tags_ids:
            tag = Tag.objects.get(id=tag_id)
            count = tag.question_set.all().count()
            tag.questions_count = count
            tag.save()

    def handle(self, *args, **options):
        self.rating_tags()
