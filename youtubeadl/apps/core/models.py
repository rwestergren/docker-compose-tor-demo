from django.db import models

from django_extensions.db.models import TimeStampedModel


class Ad(TimeStampedModel):
    TOP = 'top'
    BOTTOM = 'bottom'
    POSITION_CHOICES = (
        (TOP, 'Top'),
        (BOTTOM, 'Bottom'),
    )

    description = models.CharField(max_length=255, null=True, blank=True)
    code = models.TextField()
    position = models.CharField(max_length=10,
                                null=True,
                                blank=True,
                                choices=POSITION_CHOICES)

    def __unicode__(self):
        return self.description