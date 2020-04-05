from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from shortened_url.views import ShortenedURLListCreateAPIView, RedirectToLongURLAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Coin32 Test Project",
        default_version='v1',
        description="REST API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kylych.asankulov@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    re_path('^api/short-url/$', ShortenedURLListCreateAPIView.as_view()),
    re_path('^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0)),
    path('<str:subpart>/', RedirectToLongURLAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
