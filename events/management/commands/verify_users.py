from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from events.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Verify sample users for testing background checks'

    def handle(self, *args, **options):
        # Verify all existing users by default
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'email_verified': True,
                    'id_verified': True,
                    'contact_verified': True,
                    'account_active': True,
                }
            )
            if not created:
                profile.email_verified = True
                profile.id_verified = True
                profile.contact_verified = True
                profile.account_active = True
                profile.save()
            
            self.stdout.write(f'Verified user: {user.username}')
        
        # Create one unverified user for testing
        unverified_user, created = User.objects.get_or_create(
            username='unverified_client',
            defaults={
                'email': 'unverified@example.com',
                'user_type': 'client',
                'first_name': 'Unverified',
                'last_name': 'User'
            }
        )
        if created:
            unverified_user.set_password('password123')
            unverified_user.save()
        
        unverified_profile, created = UserProfile.objects.get_or_create(
            user=unverified_user,
            defaults={
                'email_verified': False,
                'id_verified': False,
                'contact_verified': False,
                'account_active': True,
            }
        )
        
        self.stdout.write(f'Created unverified user for testing: {unverified_user.username}')
        self.stdout.write(
            self.style.SUCCESS('Successfully updated user verification status!')
        )