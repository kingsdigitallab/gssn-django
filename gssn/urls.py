from search.views import search
from django.conf import settings
from django.conf.urls import handler404, handler500, include, url
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls

#from django.utils.functional import curry
from django.views.defaults import server_error
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.urls import include, path
from cms.views import SearchView

admin.autodiscover()

#handler404 = curry(server_error, template_name='404.html')  # noqa
#handler500 = curry(server_error, template_name='500.html')  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
]

# -----------------------------------------------------------------------------
# Wagtail CMS
# -----------------------------------------------------------------------------

urlpatterns += [
    path('wagtail/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    url(r"^search/", SearchView.as_view()),
    path('', include(wagtail_urls)),
]

# -----------------------------------------------------------------------------
# Django Debug Toolbar URLS
# -----------------------------------------------------------------------------
try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls))
        ]
except ImportError:
    pass

# -----------------------------------------------------------------------------
# Static file DEBUGGING
# -----------------------------------------------------------------------------
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
