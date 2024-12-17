from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Blog
from .serializers import BlogSerializer


# Custom pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ----------------------------
# API Views
# ----------------------------

class BlogListCreateAPIView(generics.ListCreateAPIView):
    """
    RESTful view for List and Create operations with search & filtering
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_featured"]
    search_fields = ["title", "desc", "full_article"]
    ordering_fields = ["datetime", "reading_time"]
    ordering = ["-datetime"]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles Retrieving, Updating & Deleting a single blog post
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Signal logic for cache invalidation
@receiver([post_save, post_delete], sender=Blog)
def clear_blog_cache(sender, **kwargs):
    """
    Clears cache when changes happen on Blog instance (save/delete)
    """
    cache.delete("articles")


# ----------------------------
# Template-Based Views
# ----------------------------

class HomeView(ListView):
    """
    Home page with search bar, pagination, and caching using Django Cache.
    Displays blog articles dynamically with filters applied.
    """
    model = Blog
    template_name = "blog/home.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        """
        Fetches query parameters, applies caching, and filters search logic.
        """
        query = self.request.GET.get("query", None)
        category = self.request.GET.get("category", None)
        cached_articles = cache.get("articles")

        if not cached_articles:
            queryset = super().get_queryset()
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(desc__icontains=query)
                )
            if category:
                queryset = queryset.filter(category__icontains=category)

            # Set the cache with a 5-minute expiration
            cache.set("articles", queryset, timeout=300)
        else:
            queryset = cached_articles

        return queryset

    def get_context_data(self, **kwargs):
        """
        Pass query parameters to templates for rendering filters/search bar.
        """
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query", "")
        context["category"] = self.request.GET.get("category", "")
        return context


class ArticleDetailView(DetailView):
    """
    Detail page showing a single blog's information and a list of related articles.
    """
    model = Blog
    template_name = "blog/detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        """
        Adds related articles to context for displaying recommendations on the detail page.
        """
        context = super().get_context_data(**kwargs)
        related_articles = Blog.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:5]
        context["related_articles"] = related_articles
        return context
