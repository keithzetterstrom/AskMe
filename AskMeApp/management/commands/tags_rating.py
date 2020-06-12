from django.core.cache import cache
from django.core.management.base import BaseCommand
from AskMeApp.models import Tag


class Command(BaseCommand):
    help = 'tags_rating'
    dct = {}

    def rating_tags(self):
        tags_objs = Tag.objects.all()
        for tag in tags_objs:
            count = tag.question_set.all().count()
            self.dct.update({tag.tag_name: count})

    def rating_sort(self):
        lst_d = list(self.dct.items())
        lst_d.sort(key=lambda i: i[1])
        lst_d.reverse()
        lst_tags = []
        for i in lst_d:
            lst_tags.append(i[0])
        cache.set('top100_tags', lst_tags, 300)

    def handle(self, *args, **options):
        self.rating_tags()
        self.rating_sort()
