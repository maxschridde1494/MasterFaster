from django.contrib import admin
from .models import User, Topic, Article, SubTopic

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Article)
