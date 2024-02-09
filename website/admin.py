from django.contrib import admin
from .models import BlogPost, Category, Tag, MainArea, Team, Newsletter
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(MainArea)
admin.site.register(Team)
admin.site.register(Newsletter)
