import datetime
import logging
import os
import urllib
from urlparse import urlparse, parse_qs, urlsplit, urlunsplit

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str
from django.views.generic import TemplateView, View

from braces.views import JSONResponseMixin, AjaxResponseMixin
from celery.result import AsyncResult

from youtubeadl.apps.core.utils import get_client_ip

from youtubeadl.apps.core.models import Ad
from youtubeadl.apps.downloader import tasks
from youtubeadl.apps.downloader.models import ActivityLog, Video


logger = logging.getLogger(__name__)


def download(request, youtube_id, filename):
    """
    Serves the audio file.
    """
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    file_exists = os.path.exists(filepath)

    video = None
    try:
        # We need to filter by both the youtube_id and audio_filename as the
        # record might exists but the video is still being converted.
        video = Video.objects.get(youtube_id=youtube_id, audio_filename=filename)
    except Video.DoesNotExist:
        pass

    if video and file_exists:
        ActivityLog.objects.create(
            video=video,
            action=ActivityLog.DOWNLOAD,
            client_ip=get_client_ip(request),
        )

        video.download_count += 1
        video.last_download_date = datetime.datetime.now()
        video.save()

        if settings.DEBUG:
            with open(filepath, 'rb') as file_data:
                response = HttpResponse(file_data.read(),
                                        content_type='audio/mpeg')

            response['Content-Disposition'] = 'attachment; filename={}'.format(
                smart_str(filename))
            response['Content-Length'] = os.path.getsize(filepath)

            return response
        else:
            # Have Nginx serve the file in production.
            response = HttpResponse(content_type='application/force-download')
            response['Content-Length'] = os.path.getsize(filepath)
            response['X-Accel-Redirect'] = os.path.join(settings.MEDIA_URL,
                                                        smart_str(filename))

            return response

    return HttpResponseRedirect(reverse('home'))


class DownloadFormView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(DownloadFormView, self).get_context_data()
        context['ad_top'] = Ad.objects.filter(position=Ad.TOP).first()
        context['ad_bottom'] = Ad.objects.filter(position=Ad.BOTTOM).first()

        return context


class ConvertAjaxView(JSONResponseMixin, AjaxResponseMixin, View):
    """
    Ajax view to start the video conversion.
    """

    def post_ajax(self, request, *args, **kwargs):
        url = self.parse_url(request.POST.get('url', '').strip())

        client_ip = get_client_ip(request)
        client_convert_count = ActivityLog.objects\
            .get_current_day_convert_count_by_ip(client_ip)
        daily_limit = settings.DAILY_CONVERT_LIMIT
        limit_reached = client_convert_count >= daily_limit

        if url and not limit_reached:
            task = tasks.convert.delay(url, client_ip)
            result = AsyncResult(task.id)

            # TODO: We're tying up resources here as we're waiting for the task
            # to finish. Remove this later and have the AJAX request retry
            # until result.ready().
            result.wait()

            data = {
                'task_id': task.id,
                'is_ready': False,
            }
            if result.successful():
                if result.result:
                    youtube_id = result.result['youtube_id']
                    filename = result.result['filename']
                    download_link = reverse(
                        'download_view',
                        kwargs={'youtube_id': youtube_id,
                                'filename': filename}
                    )

                    data['message'] = 'Conversion successful!'
                    data['is_ready'] = True
                    data['youtube_id'] = youtube_id
                    data['title'] = result.result['title']
                    data['filename'] = filename
                    data['download_link'] = download_link

                    return self.render_json_response(data, status=200)

                data['message'] = 'Could not convert the video. Please make ' \
                                  'sure the URL you entered is correct and ' \
                                  'the video is no more than {} minutes long.'\
                    .format(settings.MAX_DURATION_SECONDS / 60)
                return self.render_json_response(data, status=200)

            data['message'] = 'Something went wrong :('
            return self.render_json_response(data, status=500)

        if limit_reached:
            logger.warn('Client reached convert limit: %s', client_ip)
            message = "Sorry, but you've reached your daily convert limit " \
                      "of {}. Please try again tomorrow.".format(daily_limit)
            return self.render_json_response({'message': message}, status=200)

        return self.render_json_response({'message': 'Please provide a URL.'},
                                         status=200)

    def parse_url(self, url):
        """
        Remove the list parameter from the URL as we currently don't support
        conversion of an entire playlist.
        """
        qs = parse_qs(urlparse(url).query)
        if qs.get('list', None):
            del(qs['list'])
            parts = urlsplit(url)
            return urlunsplit([
                parts.scheme,
                parts.netloc,
                parts.path,
                urllib.urlencode(qs, True),
                parts.fragment
            ])

        return url