from django import forms
from .models import Event, Ticket, Sponsorship, EventReview

class EventForm(forms.ModelForm):
    """Form for creating and editing events"""
    class Meta:
        model = Event
        fields = ['name', 'description', 'category', 'location', 'date', 'time', 'price', 'max_attendees', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class TicketForm(forms.ModelForm):
    """Form for ticket booking"""
    class Meta:
        model = Ticket
        fields = ['attendee_name', 'attendee_email', 'attendee_phone']
        widgets = {
            'attendee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'attendee_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'attendee_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SponsorshipForm(forms.ModelForm):
    """Form for sponsorship donations"""
    class Meta:
        model = Sponsorship
        fields = ['company_name', 'contact_person', 'email', 'phone', 'amount', 'message', 'event', 'category']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'event': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].required = False
        self.fields['category'].required = False
        self.fields['event'].empty_label = "Select an event (optional)"
        self.fields['category'].empty_label = "Select a category (optional)"

class EventReviewForm(forms.ModelForm):
    """Form for event reviews"""
    class Meta:
        model = EventReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }