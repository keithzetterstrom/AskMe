from django.contrib import admin

from .models import Question, User, Tag

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
