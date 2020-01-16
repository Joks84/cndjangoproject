from django.contrib import admin
from .models import Post, Category, Comment, SignUp
# Register your models here.


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(SignUp)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('author', 'text')
admin.site.register(Comment, CommentAdmin)
