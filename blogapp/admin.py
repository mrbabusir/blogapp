
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "Blog Management"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Welcome to the Blog Admin"

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('title',)
    search_fields = ('title',)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'user', 'dateandtime')
    list_filter = ('post_id', 'user')
    search_fields = ('post_id__title', 'user__username')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)