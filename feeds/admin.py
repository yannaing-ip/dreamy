from django.contrib import admin
from .models import Feed, Like, Comment 
# Register your models here.
admin.site.register(Feed)
admin.site.register(Like)
admin.site.register(Comment)
