"""
URL configuration for core project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from users.views import CustomOptainToken, CustomRefreshToken

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/token/", CustomOptainToken.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", CustomRefreshToken.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
