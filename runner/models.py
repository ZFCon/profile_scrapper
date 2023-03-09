from django.db import models
from solo.models import SingletonModel


class Configuration(SingletonModel):
    runner_file = models.FileField(upload_to='runner')
    should_run = models.BooleanField(default=False)

    def __str__(self):
        return "Configuration"

    class Meta:
        verbose_name = "Configuration"