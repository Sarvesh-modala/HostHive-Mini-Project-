from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db import models
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
from .models import Event, Ticket, Offer, UserProfile, OfferLog, BackgroundCheck, Sponsorship, EventReview, EventAnalytics, Notification
from .forms import EventForm, TicketForm, SponsorshipForm, EventReviewForm

def event_list(request):
    """Display all active and approved events"""
    events = Event.objects.filter(is_active=True, approval_status='approved')
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    paginator = Paginator(events, 12)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'events/list.html', {'events': events})

def event_detail(request, pk):
    """Display event details"""
    event = get_object_or_404(Event, pk=pk, is_active=True)
    
    # Only show approved events to public, or own events to organizer
    if event.approval_status != 'approved' and event.organizer != request.user:
        messages.error(request, 'This event is not available.')
        return redirect('events:list')
    
    user_ticket = None
    if request.user.is_authenticated:
        user_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()
    
    return render(request, 'events/detail.html', {
        'event': event,
        'user_ticket': user_ticket
    })

@login_required
def event_create(request):
    """Create new event (clients only)"""
    if not request.user.is_client():
        messages.error(request, 'Only clients can create events.')
        return redirect('events:list')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully! It is now pending approval from the category host.')
            return redirect('events:detail', pk=event.pk)
    else:
        initial_data = {}
        category_id = request.GET.get('category')
        if category_id:
            initial_data['category'] = category_id
        form = EventForm(initial=initial_data)
    return render(request, 'events/form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_edit(request, pk):
    """Edit existing event (organizer only)"""
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        messages.error(request, 'You can only edit your own events.')
        return redirect('events:detail', pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Event'})

@login_required
def book_ticket(request, pk):
    """Book ticket for event with background check"""
    event = get_object_or_404(Event, pk=pk, is_active=True, approval_status='approved')
    
    # Get or create user profile for background check
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Create background check request
    bg_check, created = BackgroundCheck.objects.get_or_create(
        user=request.user,
        check_type='ticket_booking',
        status='pending'
    )
    
    # If background check is pending, show waiting message
    if bg_check.status == 'pending':
        messages.info(request, 'Your background check is pending approval from a host. Please wait for approval.')
        return redirect('events:detail', pk=pk)
    
    # If rejected, show error
    if bg_check.status == 'rejected':
        messages.error(request, f'Background check rejected: {bg_check.rejection_reason}')
        return redirect('events:detail', pk=pk)
    
    # Perform additional profile check
    if not profile.passes_background_check():
        messages.error(request, 'Your account does not meet current verification requirements for booking tickets. Please contact HostHive support.')
        return redirect('events:detail', pk=pk)
    
    if event.is_full:
        messages.error(request, 'This event is fully booked.')
        return redirect('events:detail', pk=pk)
    
    existing_ticket = Ticket.objects.filter(event=event, attendee=request.user).first()
    if existing_ticket:
        messages.info(request, 'You already have a ticket for this event.')
        return redirect('events:detail', pk=pk)
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.event = event
            ticket.attendee = request.user
            ticket.save()
            messages.success(request, 'Ticket booked successfully!')
            return redirect('events:ticket_confirmation', pk=ticket.pk)
    else:
        form = TicketForm(initial={
            'attendee_name': request.user.get_full_name() or request.user.username,
            'attendee_email': request.user.email,
        })
    
    # Get user profile for verification status display
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'events/book_ticket.html', {
        'form': form, 
        'event': event,
        'profile': profile
    })

@login_required
def ticket_confirmation(request, pk):
    """Ticket confirmation and payment"""
    ticket = get_object_or_404(Ticket, pk=pk, attendee=request.user)
    
    if request.method == 'POST':
        ticket.is_confirmed = True
        ticket.payment_status = 'confirmed'
        ticket.save()
        messages.success(request, 'Payment confirmed! Your ticket is ready.')
        return redirect('events:download_ticket', pk=ticket.pk)
    
    return render(request, 'events/ticket_confirmation.html', {'ticket': ticket})

@login_required
def download_ticket(request, pk):
    """Generate and download PDF ticket"""
    ticket = get_object_or_404(Ticket, pk=pk, attendee=request.user, is_confirmed=True)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph(f"<b>HostHive Event Ticket</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Event details
    content = f"""
    <b>Event:</b> {ticket.event.name}<br/>
    <b>Date:</b> {ticket.event.date}<br/>
    <b>Time:</b> {ticket.event.time}<br/>
    <b>Location:</b> {ticket.event.location}<br/>
    <b>Organizer:</b> {ticket.event.organizer.get_full_name() or ticket.event.organizer.username}<br/>
    <br/>
    <b>Ticket Number:</b> {ticket.ticket_number}<br/>
    <b>Attendee:</b> {ticket.attendee_name}<br/>
    <b>Email:</b> {ticket.attendee_email}<br/>
    """
    
    content_para = Paragraph(content, styles['Normal'])
    story.append(content_para)
    
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_number}.pdf"'
    return response

@login_required
def offer_approval(request):
    """Handle offer approval workflow with background check"""
    # Get pending offers for the user
    pending_offers = Offer.objects.filter(offered_to=request.user, status='pending')
    
    if not pending_offers.exists():
        messages.info(request, 'No pending offers available.')
        return redirect('events:list')
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Perform background check
    if not profile.passes_background_check():
        messages.error(request, 'Your account does not meet current verification requirements for approving offers. Please contact HostHive support.')
        return redirect('events:list')
    
    offer = pending_offers.first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            offer.status = 'approved'
            offer.save()
            profile.approval_count += 1
            profile.save()
            
            # Log the decision
            OfferLog.objects.create(
                offer=offer,
                user=request.user,
                action='approved',
                details=f'Offer approved by {request.user.username}'
            )
            
            messages.success(request, f'Offer "{offer.title}" has been approved successfully!')
            return redirect('events:offer_approval')
            
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason', '')
            offer.status = 'rejected'
            offer.rejection_reason = rejection_reason
            offer.save()
            profile.rejection_count += 1
            profile.save()
            
            # Log the decision
            OfferLog.objects.create(
                offer=offer,
                user=request.user,
                action='rejected',
                details=f'Offer rejected by {request.user.username}. Reason: {rejection_reason}'
            )
            
            messages.success(request, f'Offer "{offer.title}" has been rejected.')
            return redirect('events:offer_approval')
    
    return render(request, 'events/offer_approval.html', {
        'offer': offer,
        'profile': profile
    })

@login_required
def event_approval(request):
    """Host approval for events in their categories"""
    if not request.user.is_host():
        messages.error(request, 'Only hosts can approve events.')
        return redirect('events:list')
    
    # Get pending events in host's categories
    pending_events = Event.objects.filter(
        category__host=request.user,
        approval_status='pending',
        is_active=True
    )
    
    if not pending_events.exists():
        messages.info(request, 'No pending events for approval.')
        return redirect('categories:list')
    
    event = pending_events.first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            event.approval_status = 'approved'
            event.is_approved = True
            event.save()
            
            messages.success(request, f'Event "{event.name}" has been approved!')
            return redirect('events:event_approval')
            
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason', '')
            event.approval_status = 'rejected'
            event.rejection_reason = rejection_reason
            event.save()
            
            messages.success(request, f'Event "{event.name}" has been rejected.')
            return redirect('events:event_approval')
    
    return render(request, 'events/event_approval.html', {'event': event})

@login_required
def background_check_approval(request):
    """Host approval for background checks"""
    if not request.user.is_host():
        messages.error(request, 'Only hosts can approve background checks.')
        return redirect('events:list')
    
    # Get pending background checks
    pending_checks = BackgroundCheck.objects.filter(status='pending')
    
    if not pending_checks.exists():
        messages.info(request, 'No pending background checks.')
        return redirect('categories:list')
    
    bg_check = pending_checks.first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            bg_check.status = 'accepted'
            bg_check.reviewed_by = request.user
            bg_check.responded_at = timezone.now()
            bg_check.save()
            messages.success(request, f'Background check for {bg_check.user.username} approved!')
            return redirect('events:background_check_approval')
            
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason', 'Background check rejected by host')
            bg_check.status = 'rejected'
            bg_check.rejection_reason = rejection_reason
            bg_check.reviewed_by = request.user
            bg_check.responded_at = timezone.now()
            bg_check.save()
            messages.success(request, f'Background check for {bg_check.user.username} rejected.')
            return redirect('events:background_check_approval')
    
    return render(request, 'events/background_check_approval.html', {'bg_check': bg_check})

@login_required
def background_check_history(request):
    """View background check history"""
    checks = BackgroundCheck.objects.filter(user=request.user)
    return render(request, 'events/background_check_history.html', {'checks': checks})

@login_required
def sponsorship_create(request):
    """Create sponsorship donation"""
    if request.method == 'POST':
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sponsorship = form.save()
            
            # Create notification for hosts
            from django.contrib.auth import get_user_model
            User = get_user_model()
            hosts = User.objects.filter(user_type='host')
            for host in hosts:
                Notification.objects.create(
                    user=host,
                    notification_type='sponsorship_received',
                    title='New Sponsorship Request',
                    message=f'{sponsorship.company_name} wants to sponsor with ${sponsorship.amount}'
                )
            
            messages.success(request, 'Sponsorship request submitted successfully! Awaiting host approval.')
            return redirect('events:sponsorship_list')
    else:
        form = SponsorshipForm()
    
    return render(request, 'events/sponsorship_form.html', {'form': form, 'title': 'Submit Sponsorship'})

@login_required
def sponsorship_list(request):
    """List all sponsorships"""
    sponsorships = Sponsorship.objects.all().order_by('-created_at')
    return render(request, 'events/sponsorship_list.html', {'sponsorships': sponsorships})

@login_required
def sponsorship_approval(request):
    """Host approval for sponsorships"""
    if not request.user.is_host():
        messages.error(request, 'Only hosts can approve sponsorships.')
        return redirect('events:list')
    
    pending_sponsorships = Sponsorship.objects.filter(status='pending')
    
    if not pending_sponsorships.exists():
        messages.info(request, 'No pending sponsorships.')
        return redirect('categories:list')
    
    sponsorship = pending_sponsorships.first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            sponsorship.status = 'approved'
            sponsorship.reviewed_by = request.user
            sponsorship.approved_at = timezone.now()
            sponsorship.save()
            messages.success(request, f'Sponsorship from {sponsorship.company_name} approved!')
            return redirect('events:sponsorship_approval')
            
        elif action == 'reject':
            sponsorship.status = 'rejected'
            sponsorship.reviewed_by = request.user
            sponsorship.save()
            messages.success(request, f'Sponsorship from {sponsorship.company_name} rejected.')
            return redirect('events:sponsorship_approval')
    
    return render(request, 'events/sponsorship_approval.html', {'sponsorship': sponsorship})

@login_required
def event_review(request, pk):
    """Add review for event"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user has a confirmed ticket
    has_ticket = Ticket.objects.filter(event=event, attendee=request.user, is_confirmed=True).exists()
    if not has_ticket:
        messages.error(request, 'You can only review events you have attended.')
        return redirect('events:detail', pk=pk)
    
    # Check if user already reviewed
    existing_review = EventReview.objects.filter(event=event, user=request.user).first()
    
    if request.method == 'POST':
        form = EventReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('events:detail', pk=pk)
    else:
        form = EventReviewForm(instance=existing_review)
    
    return render(request, 'events/review_form.html', {'form': form, 'event': event})

@login_required
def dashboard(request):
    """User dashboard with analytics and notifications"""
    context = {}
    
    if request.user.is_host():
        # Host dashboard
        context.update({
            'categories': request.user.category_set.all()[:5],
            'pending_events': Event.objects.filter(category__host=request.user, approval_status='pending').count(),
            'pending_bg_checks': BackgroundCheck.objects.filter(status='pending').count(),
            'pending_sponsorships': Sponsorship.objects.filter(status='pending').count(),
            'total_revenue': Sponsorship.objects.filter(status='approved').aggregate(total=models.Sum('amount'))['total'] or 0,
        })
    elif request.user.is_client():
        # Client dashboard
        user_events = Event.objects.filter(organizer=request.user)
        context.update({
            'my_events': user_events[:5],
            'my_tickets': Ticket.objects.filter(attendee=request.user)[:5],
            'pending_events': user_events.filter(approval_status='pending').count(),
            'total_bookings': Ticket.objects.filter(event__organizer=request.user, is_confirmed=True).count(),
        })
    
    # Common data
    context.update({
        'notifications': Notification.objects.filter(user=request.user, is_read=False)[:5],
        'recent_sponsorships': Sponsorship.objects.filter(status='approved')[:3],
    })
    
    return render(request, 'events/dashboard.html', context)

@login_required
def notifications(request):
    """User notifications page"""
    user_notifications = Notification.objects.filter(user=request.user)
    
    # Mark as read when viewed
    user_notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'events/notifications.html', {'notifications': user_notifications})