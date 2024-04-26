from django.urls import path

from blog.views import BlogDeleteView, BlogDetailView, BlogListView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
