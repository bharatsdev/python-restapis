from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    """Django Command pause execution until database is not available"""

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database...")
        db_con = None
        while not db_con:
            try:
                db_con = connections['default']
            except OperationalError:
                self.stderr.write('Database unavailable, wait for 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database is ready to accept calls.'))
