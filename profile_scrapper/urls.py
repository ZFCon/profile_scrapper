from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name='runner:index', permanent=True), name="index"),
    path("admin/", admin.site.urls),
    path("runner/", include(("runner.urls", "runner"), namespace="runner")),
]


# serve static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# serve media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)