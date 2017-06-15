from django.contrib import admin
from .models import User, Topic, Article, SubTopic, Video

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Article)
admin.site.register(Video)
