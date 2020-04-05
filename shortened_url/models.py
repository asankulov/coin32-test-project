from django.db import models


class ShortenedURL(models.Model):
    subpart = models.CharField(verbose_name='Subpart', max_length=100, unique=True, db_index=True)
    long_url = models.URLField(verbose_name='Long URL')
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Shortened URL'
        verbose_name_plural = 'Shortened URLs'
        ordering = ['-created_at']

