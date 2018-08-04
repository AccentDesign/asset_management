from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from app import api, routers
from app.views import HomeView
from assets.urls import router as assets_router
from authentication.urls import router as authentication_router


# api and docs
api_title = 'Asset Management API'
schema_view = get_schema_view(title=api_title)

router = routers.DefaultRouter()

# external routes
router.register(r'images', api.ImageRenditionViewSet)

# internal routes
router.extend(assets_router)
router.extend(authentication_router)

# urls
urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'api'))),
    path('api/docs/', include_docs_urls(title=api_title)),
    path('api/oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('authentication.urls')),
    path('', HomeView.as_view(), name='home'),
    path('', include('assets.urls'))
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
