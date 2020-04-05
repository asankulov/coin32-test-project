from datetime import timedelta

from django.db import IntegrityError
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from shortened_url.exceptions import SubpartAlreadyTakenException
from shortened_url.models import ShortenedURL
from redis import Redis, ConnectionPool
from django.conf import settings


class ShortenedURLService:
    @staticmethod
    def shorten_url(data, session_id):
        subpart = data.get('subpart', None)
        shortened_url_instance = ShortenedURL(long_url=data['long_url'], user_id=session_id)

        if subpart is not None:
            try:
                shortened_url_instance.subpart = subpart
                shortened_url_instance.save()
                return shortened_url_instance.subpart

            except IntegrityError:
                raise SubpartAlreadyTakenException

        shortened_url_instance.subpart = get_random_string(7)
        shortened_url_instance.save()

        cache_service = CacheService()
        cache_service.save_in_cache(
            shortened_url_instance.subpart,
            shortened_url_instance.long_url,
            settings.SHORT_URL_LIFETIME
        )

        return shortened_url_instance.subpart

    @staticmethod
    def get_long_url(subpart):
        cache_service = CacheService()
        long_url = cache_service.get_from_cache(subpart)

        if long_url is not None:
            return long_url
        try:
            shortened_url_instance = ShortenedURL.objects.get(subpart=subpart)
            return shortened_url_instance.long_url

        except ShortenedURL.DoesNotExist:
            return None

    @staticmethod
    def remove_expired_rows():
        return ShortenedURL.objects.annotate(
            expires_at=ExpressionWrapper(F('created_at') + timedelta(seconds=settings.SHORT_URL_LIFETIME),
                                         output_field=DateTimeField())
        ).filter(expires_at__lte=timezone.now()).delete()


class CacheService:
    def __init__(self):
        self.r = Redis(connection_pool=ConnectionPool().from_url(settings.CACHE_SERVER_URL))

    def save_in_cache(self, key, value, expiration_time):
        return self.r.setex(key, expiration_time, value)

    def get_from_cache(self, key):
        value = self.r.get(key)
        if value is not None:
            return value.decode('utf-8')
        return value
