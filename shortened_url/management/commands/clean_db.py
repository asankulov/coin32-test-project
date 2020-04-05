from django.core.management.base import BaseCommand

from shortened_url.services import ShortenedURLService


class Command(BaseCommand):

    help = 'Delete obsolete urls from db'

    def handle(self, *args, **options):
        result = ShortenedURLService.remove_expired_rows()
        self.stdout.write(self.style.SUCCESS(f'Result: {result}'))

    def execute(self, *args, **options):
        super().execute(*args, **options)
        return 0
