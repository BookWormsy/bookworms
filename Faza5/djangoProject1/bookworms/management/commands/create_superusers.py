import os
import json
from django.core.management.base import BaseCommand
from bookworms.models import UsernamesPasswords  # You should import the model, not the manager
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create superusers from JSON fixture file with hashed passwords'

    def handle(self, *args, **options):
        fixture_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'superuser_fixture.json'
        )
        with open(fixture_path, 'r') as fixture_file:
            superusers_data = json.load(fixture_file)

        for superuser_data in superusers_data:
            email = superuser_data['fields'].get('email', '')
            username = superuser_data['fields']['username']
            password = superuser_data['fields']['password']
            UsernamesPasswords.objects.create_superuser(username, email, password)  # Use the manager via the model

        self.stdout.write(self.style.SUCCESS('Superusers created successfully.'))
