import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    """ Django command that waits for database to be available """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')

        for _ in range(20):
            try:
                connection.ensure_connection()
                break
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 5 second...')
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('Database available!'))
