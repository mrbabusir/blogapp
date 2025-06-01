from django_filters import FilterSet
from .models import Blog, Comment

class BlogFilter(FilterSet):
    class Meta:
        model = Blog
        fields = {
            'user': ['exact'],
            'title': ['exact', 'icontains'],
        }
class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'user': ['exact'],
            'post_id': ['exact'],   # Filter by the blog post ID
        }