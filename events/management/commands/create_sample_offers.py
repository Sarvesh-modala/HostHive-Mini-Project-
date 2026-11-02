from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from events.models import Event, Offer, UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample offers and user profiles for testing'

    def handle(self, *args, **options):
        # Create user profiles for existing users
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
            if created:
                self.stdout.write(f'Created profile for {user.username}')

        # Create sample offers
        try:
            client1 = User.objects.get(username='client1')
            host1 = User.objects.get(username='host1')
            event = Event.objects.first()
            
            if event:
                offer, created = Offer.objects.get_or_create(
                    title='Venue Sponsorship Opportunity',
                    defaults={
                        'description': 'We would like to sponsor your event venue and provide catering services.',
                        'offer_type': 'sponsorship',
                        'event': event,
                        'offered_by': host1,
                        'offered_to': client1,
                        'amount': 500.00,
                        'status': 'pending'
                    }
                )
                if created:
                    self.stdout.write(f'Created sample offer: {offer.title}')
                
        except User.DoesNotExist:
            self.stdout.write('Sample users not found. Run populate_data first.')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample offers and profiles!')
        )