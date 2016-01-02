from django.contrib import admin
from django.utils.text import Truncator

from youtubeadl.apps.downloader import models


class ActivityLogInline(admin.TabularInline):
    model = models.ActivityLog
    readonly_fields = ('created',)


@admin.register(models.ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        'video',
        'video_title',
        'client_ip',
        'action',
        'created',
    )
    list_filter = ('action', 'client_ip')

    def video_title(self, obj):
        return Truncator(obj.video.title).chars(50)
    video_title.admin_order_field = 'video__title'


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'youtube_id',
        'title',
        'audio_filename',
        'duration',
        'download_count',
        'last_download_date',
    )
    list_filter = ('last_download_date',)
    search_fields = (
        'youtube_id',
        'title',
        'audio_filename',
    )

    inlines = [ActivityLogInline]
