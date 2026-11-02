from django.contrib import admin
from .models import Event, Ticket, Offer, UserProfile, OfferLog, BackgroundCheck, Sponsorship, EventReview, EventAnalytics, Notification

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Event model"""
    list_display = ('name', 'category', 'organizer', 'date', 'time', 'approval_status', 'available_spots', 'is_active')
    list_filter = ('category', 'date', 'approval_status', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'organizer__username', 'location')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Ticket model"""
    list_display = ('ticket_number', 'event', 'attendee_name', 'is_confirmed', 'payment_status', 'created_at')
    list_filter = ('is_confirmed', 'payment_status', 'created_at', 'event__category')
    search_fields = ('ticket_number', 'attendee_name', 'attendee_email', 'event__name')
    readonly_fields = ('ticket_number', 'created_at')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin interface for Offer model"""
    list_display = ('title', 'offer_type', 'event', 'offered_by', 'offered_to', 'status', 'created_at')
    list_filter = ('offer_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'event__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model"""
    list_display = ('user', 'email_verified', 'id_verified', 'contact_verified', 'account_active', 'approval_count', 'rejection_count', 'passes_background_check')
    list_filter = ('email_verified', 'id_verified', 'contact_verified', 'account_active')
    search_fields = ('user__username', 'user__email')
    
    def passes_background_check(self, obj):
        return obj.passes_background_check()
    passes_background_check.boolean = True
    passes_background_check.short_description = 'Passes Check'

@admin.register(BackgroundCheck)
class BackgroundCheckAdmin(admin.ModelAdmin):
    """Admin interface for BackgroundCheck model"""
    list_display = ('user', 'check_type', 'status', 'reviewed_by', 'requested_at', 'responded_at')
    list_filter = ('status', 'check_type', 'requested_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('requested_at',)

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    """Admin interface for Sponsorship model"""
    list_display = ('company_name', 'amount', 'status', 'reviewed_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('company_name', 'contact_person', 'email')
    readonly_fields = ('created_at',)

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    """Admin interface for EventReview model"""
    list_display = ('event', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('event__name', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(EventAnalytics)
class EventAnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for EventAnalytics model"""
    list_display = ('event', 'views', 'bookings', 'revenue', 'last_updated')
    readonly_fields = ('last_updated',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model"""
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at',)

@admin.register(OfferLog)
class OfferLogAdmin(admin.ModelAdmin):
    """Admin interface for OfferLog model"""
    list_display = ('offer', 'user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('offer__title', 'user__username')
    readonly_fields = ('timestamp',)