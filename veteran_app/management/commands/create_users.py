from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create multiple users from list'

    def handle(self, *args, **options):
        users = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@email.com'},
            {'username': 'user2', 'password': 'pass456', 'email': 'user2@email.com'},
        ]
        
        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_active': True
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f"Created user: {user.username}")
            else:
                self.stdout.write(f"User exists: {user.username}")