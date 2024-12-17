from django.urls import path
from .views import (
    BlogListCreateAPIView,
    BlogRetrieveUpdateDestroyAPIView,
    HomeView,
    ArticleDetailView,
)

app_name = "blog"

urlpatterns = [
    # Home page view: Displays the list of articles with filters & search
    path("", HomeView.as_view(), name="home"),
    
    # Article Detail Page
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    
    # REST API - List & Create blog entries
    path("api/blogs/", BlogListCreateAPIView.as_view(), name="blog-list-create"),
    
    # REST API - Retrieve, Update & Destroy blog entries by primary key
    path("api/blogs/<int:pk>/", BlogRetrieveUpdateDestroyAPIView.as_view(), name="blog-retrieve-update-destroy"),
]
