import uuid

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.all().delete()
        user = User.objects.create(
            email='admin@gmail.com',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('password')
        user.save()
