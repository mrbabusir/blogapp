from django.shortcuts import render
from django.http import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from datetime import datetime
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.mixins import RetrieveModelMixin,status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.contrib.auth  import get_user_model
from .permission import IsAuthorOrReadonly


User = get_user_model() # get_user_model() le custom user model lai fetch garne kaam garchha    

# Create your views here.
class PaginationView(PageNumberPagination): # pagination was not working in GenericAPIView so created a custom pagination view for esp in commentList view
    '''Custom pagination view to handle pagination settings.'''
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum allowed page size

class CategoryListView(GenericAPIView):
    '''CategoryList view to handle listing and creating categories.'''
    queryset = Category.objects.all().order_by('id') # category ko sabai data liyera queryset ma rakheko
    serializer_class = CategorySerializer # category serializer ko class banko
    pagination_class = PaginationView # pagination ko lagi custom pagination class use gareko
    permission_classes = [IsAuthenticatedOrReadOnly] # permission_classes le authenticated user lai matra access dincha, ani read only access haru lai pani allow garchha
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['category_name'] # filter_backends le search and filter ko lagi use garne
    def post(self, request):
        '''Create a new Category'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) # serializer ko data validate garna parcha
        serializer.save(user=request.user) # user ko data save garna parcha
        # permission_classes = [IsAuthenticated]
        return Response({"status": "New Category Created."}, status=status.HTTP_201_CREATED)


    def get(self, request):
        ''''List all categories with pagination.'''
        queryset =self.filter_queryset(self.get_queryset()) # queryset ko data filter garne
        page = self.paginate_queryset(queryset) #paginate_queryset inbuilt method ho jasley quryset lai paginate garne kaam garchha
        if page is not None: # page ko value null na bhaye pagination garna parcha
            serializer = self.get_serializer(page, many=True) # page ko instance lai serialize gareko
            return self.get_paginated_response(serializer.data) # paginated response return gareko
        serializer = self.get_serializer(self.get_queryset(), many=True) #fetching all serialized data from blogs #get_queryset() le queryset ko data return garchha
        return Response(serializer.data)
        
        
class CategoryDetailView(GenericAPIView):
    '''CategoryDetailView to handle retrieving a specific category.'''
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        '''Retrieve a specific category by its ID.'''
        category = get_object_or_404(Category, pk=pk) # pk ko basis ma Category model ko objects fetch gareko
        serializer = self.get_serializer(category) # serializer ko instance haru lai serializer garna parcha
        return Response(serializer.data) # category ko data return garreko

class BlogList(GenericAPIView):
    '''BlogList view to handle listing and creating blog posts.'''
    queryset = Blog.objects.all().order_by('id') # blog ko sabai data liyera queryset ma rakheko..order by le id ko basis ma order ma rakheko
    serializer_class = BlogListSerializer #blogserializer ko serilizer class banko
    pagination_class = PaginationView #genericapiview ma settings bata pagination hundaina tesaile import garera pagination_class banako
    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter) # filter_backends le search and filter ko lagi use garne
    search_fields = ['title'] # search_fields le title ma search garne
    filterset_fields = ['user',]
    ordering_fields = ['dateandtime', 'id'] # filterset_fields le user ma filter garne
    permission_classes = [IsAuthenticatedOrReadOnly] # permission_classes le authenticated user lai matra access dincha, ani read only access haru lai pani allow garchha
    @extend_schema(
        parameters=[
            OpenApiParameter(name='title', description='Filter by title', required=False, type=str),
        ]
    )
    def get(self, request): # Get paginated queryset
        queryset = self.filter_queryset(self.get_queryset()) # queryset ko data filter garne
        page = self.paginate_queryset(queryset) #paginate_queryset inbuilt method ho jasley quryset lai paginate garne kaam garchha
        if page is not None: # page ko value null na bhaye pagination garna parcha
            serializer = self.get_serializer(page, many=True) # page ko instance lai serialize gareko
            return self.get_paginated_response(serializer.data) # paginated response return gareko   
        serializer = self.get_serializer(self.get_queryset(), many=True) #fetching all serialized data from blogs #get_queryset() le queryset ko data return garchha
        return Response(serializer.data)
    def post(self, request):
        '''Create a new blog post.'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) # serializer ko data validate garna parcha
        serializer.save(user=request.user) # user ko data save garna parcha
        # permission_classes = [IsAuthenticated]
        return Response({"status": "published"}, status=status.HTTP_201_CREATED)

class BlogDetailView(GenericAPIView):
    '''BlogDetailView to handle retrieving, updating, and deleting a specific blog post.'''
    queryset = Blog.objects.prefetch_related('comments','category')# blog data and comments lai queryset ma rakheko#prefect inbuilt function ho jasle related data lai fetch garne kaam garchha
    serializer_class = BlogDetailSerializer
    permission_classes = [IsAuthorOrReadonly]
    def get (self, request,pk):
        try:
            blog = self.get_object() # pk ko basis ma Blog model ko objects fetch gareko
            serializer = self.get_serializer(blog, context = {'request': request}) # serializer ko instance haru lai serializer garna parcha
        except Blog.DoesNotExist:
            return Response("detail: Blog not found", status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data) # blog ko data return garreko
    def put(self, request, pk):
        blog = self.get_object()
        serializer = self.get_serializer(blog, data=request.data) # serializer ko instance haru lai serializer garna parcha
        serializer.is_valid(raise_exception=True) # serializer ko data validate garna parcha
        serializer.save() # serializer ko data save garna parcha
        return Response(serializer.data) # blog ko data return garreko
    def patch(self, request, pk): ##removed put fucntion beause patch le sabai field haru update ani partially pani updated garne kaam garchha
        blog = self.get_object()  # Auto 404 if not found
        serializer = self.get_serializer(blog, data=request.data, partial=True) # partial=True le only updated fields matra update garne kaam garchha
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        blog = self.get_object()  # Auto 404 if not found
        blog.delete()
        return Response('detail : Blog is Deleted', status=status.HTTP_204_NO_CONTENT)

   
class CommentList(GenericAPIView):
    '''CommentList view to handle listing and creating comments.'''

    queryset = Comment.objects.select_related('user', 'post_id').all().order_by('id') # get all comments and related user and post_id data#select_related le related data lai fetch garne kaam garchha
    serializer_class = CommentSerializer # serializer class for comments
    pagination_class = PaginationView #genericapiview ma settings bata pagination hundaina tesaile import garera pagination_class banako 
    filter_backends = [filters.SearchFilter, DjangoFilterBackend] # filter_backends le search and filter ko lagi use garne
    search_fields = ['comment',] # search_fields le comment ma search garne
    filterset_fields = ['user',] # filterset_fields le user ma filter garne
    permission_classes = [IsAuthenticatedOrReadOnly] # permission_classes le authenticated user lai matra access dincha, ani read only access haru lai pani allow garchha
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    # def post(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)
    #     return Response(
    #         {"status": "published"},
    #         status=status.HTTP_201_CREATED
    #     ) 
class CommentDetailView(GenericAPIView):
    queryset = Comment.objects.all() # get all comments
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadonly]
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)   
    def put(self, request, pk):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def patch(self, request,blog_pk, pk):
        comment = self.get_object()
        serializer = self.get_serializer(
            comment, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request,blog_pk, pk):
        comment = self.get_object()
        comment.delete()
        return Response(
            {"detail": "Comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
# class BlogCommentsView(GenericAPIView): #
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     def get(self, request, pk):
#         comments = self.queryset.filter(Comment=pk)
#         serializer = self.serializer_class(comments, many=True)
#         return Response(serializer.data)
    