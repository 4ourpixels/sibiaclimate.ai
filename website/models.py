from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.templatetags.static import static

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    youtube = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="blog/",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    @property
    def get_blog_url(self):
        return f"www.sibiaclimate.ai/{self.slug}/"

    @property
    def get_og_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        else:
            default_image_path = 'images/sibia-climate-ai-thumbnail.jpg'
            return static(default_image_path)


class BlogPhoto(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image_credit = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    blog = models.ForeignKey(
        BlogPost, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(
        null=False,
        blank=False,
        upload_to="blog/",
    )
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.blog.title}"


class AboutUsPage(models.Model):
    footer_about = models.TextField(null=True, blank=True)
    what_we_do = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return "About Us"
    
    

class MainArea(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="main-areas/",
    )
    slug = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def get_area_url(self):
        return f"www.sibiaclimate.ai/main-area/{self.slug}/"
    
    @property
    def get_url(self):
        return reverse("main_area_detail", kwargs={"slug": self.slug})

    @property
    def get_og_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        else:
            default_image_path = 'images/sibia-climate-ai-thumbnail.jpg'
            return static(default_image_path)


class Team(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="team/", null=True, blank=True)
    twitter = models.TextField(blank=True, null=True)
    facebook = models.TextField(blank=True, null=True)
    instagram = models.TextField(blank=True, null=True)
    linkedin = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} | {self.user.first_name}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Newsletter(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email
