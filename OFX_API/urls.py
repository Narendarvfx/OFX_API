#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, reverse_lazy
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from django.contrib.auth import views as auth_views

from OFX_API import views


schema_view = get_schema_view(
    openapi.Info(
        title="OFX API",
        default_version='v1',
        description="Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="narendarreddy.gunreddy@oscarfx.com"),
        license=openapi.License(name="OFX License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('wsapi/', include('wsapi.urls')),
    # path('wsdoc/', include('wsdoc.urls')),
    url(r'^$', views.home_view, name='home_view'),
    url(r'^home/$', views.home_view, name='home'),

path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
  html_email_template_name='registration/password_reset_html_email.html', template_name='registration/password_reset_form.html'
)),
path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'
)),
path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'
)),
path('accounts/password_reset/', auth_views.PasswordResetView.as_view(success_url = reverse_lazy('password_reset_done')), name='password_reset'),
path('accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('hrm.urls')),
    url(r'^', include('production.urls')),
    url(r'^', include('essl.urls')),
    url(r'^', include('wsnotifications.urls')),
    url(r'^', include('ofx_dashboards.urls')),
    url(r'^', include('ofx_statistics.urls')),
    url(r'^', include('time_management.urls')),
    url(r'^', include('dynamicfilters.urls')),
    url(r'^', include('production.v2.urls')),
    url(r'^', include('shotassignments.urls')),
    url(r'^', include('pipeline_api.urls')),
    url(r'^', include('history.urls')),

    # url(r'^', include('review.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='OFX API')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('logs/', include('log_viewer.urls')),
    url(r'^health_check/', include('health_check.urls')),

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
