from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates default permission groups for users'

    def handle(self, *args, **options):
        from ... import permissions
