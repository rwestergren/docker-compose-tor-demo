from django.contrib import admin

from youtubeadl.apps.core.models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('description', 'position', 'created', 'modified')