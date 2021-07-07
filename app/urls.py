from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import HomeView

# urls
urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('explorer/', include('explorer.urls')),
    path('', HomeView.as_view(), name='home'),
    path('', include('assets.urls'))
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
