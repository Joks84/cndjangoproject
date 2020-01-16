from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cn_app:post_list', kwargs={'pk':self.pk})

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default = None)
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cn_app:post_detail', kwargs=(self.pk))

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    author = models.CharField(max_length = 100)
    text = models.CharField(max_length = 500)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment: {} by {}'.format(self.text, self.author)

class SignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
