from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from categories.models import Category

User = get_user_model()

class Event(models.Model):
    """Event model with comprehensive details and ticket management"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'client'})
    location = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_attendees = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to='images/events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    approval_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
    
    @property
    def available_spots(self):
        return self.max_attendees - self.ticket_set.filter(is_confirmed=True).count()
    
    @property
    def is_full(self):
        return self.available_spots <= 0

class Ticket(models.Model):
    """Ticket model for event registrations"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length=15, blank=True)
    ticket_number = models.CharField(max_length=20, unique=True)
    is_confirmed = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'attendee']
    
    def __str__(self):
        return f'{self.ticket_number} - {self.event.name}'
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            import uuid
            self.ticket_number = f'TK{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

class Offer(models.Model):
    """Offer model for event partnerships and sponsorships"""
    OFFER_TYPES = [
        ('sponsorship', 'Sponsorship'),
        ('partnership', 'Partnership'),
        ('venue', 'Venue Offer'),
        ('service', 'Service Offer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='offers')
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')
    offered_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} - {self.event.name}'

class UserProfile(models.Model):
    """Extended user profile for background checks"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    id_verified = models.BooleanField(default=False)
    contact_verified = models.BooleanField(default=False)
    account_active = models.BooleanField(default=True)
    approval_count = models.PositiveIntegerField(default=0)
    rejection_count = models.PositiveIntegerField(default=0)
    
    def passes_background_check(self):
        return (self.account_active and 
                self.email_verified and 
                self.contact_verified and
                self.rejection_count < 5)
    
    def get_verification_status(self):
        """Get detailed verification status for display"""
        return {
            'email_verified': self.email_verified,
            'contact_verified': self.contact_verified,
            'id_verified': self.id_verified,
            'account_active': self.account_active,
            'rejection_count': self.rejection_count,
            'passes_check': self.passes_background_check()
        }

class BackgroundCheck(models.Model):
    """Background check requests and history"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_checks')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_checks')
    check_type = models.CharField(max_length=50, default='ticket_booking')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.check_type} - {self.status}'

class Sponsorship(models.Model):
    """Sponsorship donations for events and categories"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        target = self.event.name if self.event else self.category.name
        return f'{self.company_name} - ${self.amount} for {target}'

class EventReview(models.Model):
    """User reviews and ratings for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.rating}★ for {self.event.name}'

class EventAnalytics(models.Model):
    """Analytics tracking for events"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    bookings = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Analytics for {self.event.name}'

class Notification(models.Model):
    """User notifications system"""
    NOTIFICATION_TYPES = [
        ('event_approved', 'Event Approved'),
        ('event_rejected', 'Event Rejected'),
        ('sponsorship_received', 'Sponsorship Received'),
        ('background_check', 'Background Check Update'),
        ('ticket_booked', 'Ticket Booked'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} - {self.user.username}'

class OfferLog(models.Model):
    """Audit log for offer decisions"""
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)