from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='list'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('create/', views.event_create, name='create'),
    path('<int:pk>/edit/', views.event_edit, name='edit'),
    path('<int:pk>/book/', views.book_ticket, name='book_ticket'),
    path('ticket/<int:pk>/confirm/', views.ticket_confirmation, name='ticket_confirmation'),
    path('ticket/<int:pk>/download/', views.download_ticket, name='download_ticket'),
    path('offers/', views.offer_approval, name='offer_approval'),
    path('approve/', views.event_approval, name='event_approval'),
    path('background-approval/', views.background_check_approval, name='background_check_approval'),
    path('background-history/', views.background_check_history, name='background_check_history'),
    path('sponsorship/create/', views.sponsorship_create, name='sponsorship_create'),
    path('sponsorship/', views.sponsorship_list, name='sponsorship_list'),
    path('sponsorship/approve/', views.sponsorship_approval, name='sponsorship_approval'),
    path('<int:pk>/review/', views.event_review, name='event_review'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications, name='notifications'),
]