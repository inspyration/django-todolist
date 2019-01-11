"""## finances URL Configuration"""


from django.conf import settings
from django.contrib import admin
from django.urls import path, include

if settings.DEBUG:
    import debug_toolbar


urlpatterns = [  # pylint: disable=invalid-name
    path('i18n/', include('django.conf.urls.i18n')),
    path('', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns  # pylint: disable=invalid-name
