from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "status": "Backend running",
        "app": "NexScan AI",
        "version": "1.0"
    })

urlpatterns = [
     path("", root_view),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )