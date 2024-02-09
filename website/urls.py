from django.urls import path
from .views import index, blog_detail, blog_list, edit_blog, add_blog, main_areas, main_area_detail, about, newsletter, logoutUser

urlpatterns = [
    path('', index, name='index'),
    path('blogs', blog_list, name='blog_list'),
    path('newsletter', newsletter, name='newsletter'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('blog/edit-blog/<slug:slug>/', edit_blog, name='edit_blog'),
    path('blog/add-blog/', add_blog, name='add_blog'),
    path('main-areas/', main_areas, name='main_areas'),
    path('about-us/', about, name='about'),
    path('main-area/<slug:slug>/', main_area_detail, name='main_area_detail'),
    path('logout/', logoutUser, name='logout'),
]
