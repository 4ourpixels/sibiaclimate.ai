from django.urls import path
from .views import index, blog_detail, blog_list, edit_blog, add_blog

urlpatterns = [
    path('', index, name='index'),
    path('blogs', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('edit-blog/<slug:slug>/', edit_blog, name='edit_blog'),
    path('add-blog/', add_blog, name='add_blog'),
]
