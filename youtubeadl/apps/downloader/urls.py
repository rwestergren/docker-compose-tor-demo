from django.conf.urls import patterns, url

from youtubeadl.apps.downloader import views


urlpatterns = patterns('',
    url(
        regex=r'^convert/$',
        view=views.ConvertAjaxView.as_view(),
        name='convert_ajax_view',
    ),
    url(
        regex=r'^download/(?P<youtube_id>.*)/(?P<filename>.*)$',
        view=views.download,
        name='download_view',
    ),
)