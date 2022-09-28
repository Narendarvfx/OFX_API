from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from OFX_API import views

schema_view = get_schema_view(
    openapi.Info(
        title="OFX API",
        default_version='v1',
        description="Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="narendar.g@ofxvfx.com"),
        license=openapi.License(name="OFX License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^$', views.home_view, name='home_view'),
    url(r'^home/$', views.home_view, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('profiles.urls')),
    url(r'^', include('hrm.urls')),
    url(r'^', include('production.urls')),
    url(r'^', include('essl.urls')),
    url(r'^', include('notifications.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='OFX Api')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('logs/', include('log_viewer.urls')),
    path('profileview/',views.profile_view, name='profileview'),

]
handler400 = views.bad_request
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.server_error

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns = [
        url(r'^debug/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Admin Site Config
admin.sites.AdminSite.site_header = 'ShotBuzz Admin Portal'
admin.sites.AdminSite.site_title = 'ShotBuzz Admin Portal'
admin.sites.AdminSite.index_title = 'ShotBuzz -- Ease of Production'
