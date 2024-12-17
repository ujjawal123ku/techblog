from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from list import urls as list_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(list_urls)),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
