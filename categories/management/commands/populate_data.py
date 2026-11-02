from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from events.models import Event
from datetime import date, time, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Create sample users
        host1, created = User.objects.get_or_create(
            username='host1',
            defaults={
                'email': 'host1@example.com',
                'user_type': 'host',
                'first_name': 'John',
                'last_name': 'Host'
            }
        )
        if created:
            host1.set_password('password123')
            host1.save()

        client1, created = User.objects.get_or_create(
            username='client1',
            defaults={
                'email': 'client1@example.com',
                'user_type': 'client',
                'first_name': 'Jane',
                'last_name': 'Client'
            }
        )
        if created:
            client1.set_password('password123')
            client1.save()

        # Create sample categories
        categories_data = [
            {
                'name': 'Music & Concerts',
                'description': 'Live music performances, concerts, and musical events for all genres.',
                'host': host1
            },
            {
                'name': 'Technology & Innovation',
                'description': 'Tech conferences, workshops, and innovation meetups.',
                'host': host1
            },
            {
                'name': 'Food & Dining',
                'description': 'Culinary experiences, food festivals, and dining events.',
                'host': host1
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Athletic events, fitness classes, and sports competitions.',
                'host': host1
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample events
        music_category = Category.objects.get(name='Music & Concerts')
        tech_category = Category.objects.get(name='Technology & Innovation')

        events_data = [
            {
                'name': 'Summer Jazz Festival',
                'description': 'Join us for an evening of smooth jazz under the stars.',
                'category': music_category,
                'organizer': client1,
                'location': 'Central Park Amphitheater',
                'date': date.today() + timedelta(days=30),
                'time': time(19, 0),
                'price': 25.00,
                'max_attendees': 200
            },
            {
                'name': 'AI & Machine Learning Workshop',
                'description': 'Hands-on workshop covering the latest in AI and ML technologies.',
                'category': tech_category,
                'organizer': client1,
                'location': 'Tech Hub Conference Center',
                'date': date.today() + timedelta(days=15),
                'time': time(10, 0),
                'price': 50.00,
                'max_attendees': 50
            }
        ]

        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                name=event_data['name'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )