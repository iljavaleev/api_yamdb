from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('api.urls')),
#     path('schema/', SpectacularAPIView.as_view(), name='schema'),
#     path(
#         'schema/redoc/',
#         SpectacularRedocView.as_view(url_name='schema'),
#         name='redoc',
#     ),
#     path(
#         'schema/swagger-ui/',
#         SpectacularSwaggerView.as_view(url_name='schema'),
#         name='swagger-ui',
#     ),
# ]