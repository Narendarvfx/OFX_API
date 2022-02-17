from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from OFX_API import views

urlpatterns = [
    url(r'^$', views.home_view, name='home_view'),
    url(r'^home/$', views.home_view, name='home'),
    url(r'^', include('profiles.urls')),
    url(r'^', include('hrm.urls')),
    url(r'^', include('production.urls')),
    url(r'^', include('essl.urls')),
    url(r'^', include('notifications.urls')),
    path('admin/', admin.site.urls),
    path('admin/log_viewer/', include('log_viewer.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns = [
        url(r'^debug/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Admin Site Config
admin.sites.AdminSite.site_header = 'OFX API'
admin.sites.AdminSite.site_title = 'OFX API'
admin.sites.AdminSite.index_title = 'OFX A Complete Studio Pipeline'
