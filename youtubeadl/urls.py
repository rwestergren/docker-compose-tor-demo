from django.conf.urls import include, url
from django.contrib import admin

from youtubeadl.apps.downloader.views import DownloadFormView


admin.site.site_header = 'YouTube ADL Admin'
admin.site.site_title = 'YouTube ADL Admin'

urlpatterns = [
    url(r'^$', DownloadFormView.as_view(), name='home'),
    url(r'^downloader/', include('youtubeadl.apps.downloader.urls')),

    # Grappelli needs to be defined before the admin.
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
