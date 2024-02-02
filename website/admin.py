from django.contrib import admin
from .models import BlogPost, Category, Tag
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Category)
