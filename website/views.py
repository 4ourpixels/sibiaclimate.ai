from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, BlogPost, MainArea, Team, Newsletter
from .forms import BlogForm, NewsletterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
all_main_areas = MainArea.objects.all()

def blog_list(request):
    title_tag = "Blogs"
    context = {
        'title_tag': title_tag,
        'blogs': BlogPost.objects.all(),
    }
    return render(request, 'blog/blog-list.html', context)


def index(request):
    title_tag = "Home"
    members = Team.objects.all()
    context = {
        'title_tag': title_tag,
        'all_main_areas': all_main_areas,
        'members': members,
    }
    return render(request, 'index.html', context)


def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    keywords = [
        item.strip()
        for item in blog.meta_keywords.split(',')
        if item.strip()
    ]

    context = {
        'title_tag': blog.title,
        'meta_keywords':  blog.summary,
        'meta_description': blog.meta_keywords,
        'keywords': keywords,
        'blog': blog,
    
    }
    return render(request, 'blog/blog-detail.html', context)


def edit_blog(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    title_tag = f"Update: {blog.title}"
    if request.method == 'POST':
        edit_blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        if edit_blog_form.is_valid():
            edit_blog_form.save()
            messages.info(request, f'"{blog.title}" update was successful!')
            return redirect('blog_detail', slug)
        else:
            print("Errors occurred while uploading: ",
                  edit_blog_form.errors)
    else:
        edit_blog_form = BlogForm(instance=blog)

    context = {
        'edit_blog_form': edit_blog_form,
        'title_tag': title_tag,
        'blog': blog,
    }

    return render(request, 'edit-blog.html', context)


@login_required(login_url='login')
def add_blog(request):
    title_tag = "Add new blog"

    if request.method == 'POST':
        new_blog_form = BlogForm(request.POST, request.FILES)
        if new_blog_form.is_valid():
            new_blog = new_blog_form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            messages.info(request, f'"{new_blog.title}" was added!')
            return redirect('blog_detail', new_blog.tag.slug, new_blog.slug)
    else:
        new_blog_form = BlogForm()

    context = {
        'title_tag': title_tag,
        'new_blog_form': new_blog_form
    }

    return render(request, 'blog/add-blog.html', context)

def main_areas(request):
    context = {
        'title_tag': "Main Areas",
        'all_main_areas': all_main_areas,
    }
    return render(request, 'main-areas.html', context)

def main_area_detail(request, slug):
    area_detail = get_object_or_404(MainArea, slug=slug)
    context = {
        'title_tag': area_detail.title,
        'area_detail': area_detail,
        'all_main_areas': all_main_areas,
    }
    return render(request, 'main-area-detail.html', context)

def newsletter(request):
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data.get('email')
            if Newsletter.objects.filter(email=email).exists():
                messages.info(
                    request, "You're already one of our favorites! Keep an eye on your inbox for more amazing content.")
            else:
                newsletter_form.save()
                print(f"{email} subscribed to our newsletter!")
                messages.success(
                    request, "Stay tuned for the latest news and insider tips we've got lined up just for you.")
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer or 'index')
    else:
        newsletter_form = NewsletterForm()

    context = {
        'title_tag': "Newsletter",
        'newsletter_form': newsletter_form,
    }

    return render(request, 'newsletter.html', context)

def about(request):
    context = {
        'title_tag': "About Us",
        'members': Team.objects.all(),
    }
    return render(request, 'about.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')
