from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='password'
        )

        User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='password'
        )

        User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='password'
        )