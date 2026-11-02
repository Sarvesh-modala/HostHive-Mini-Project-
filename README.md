# HostHive - Event Management Platform

HostHive is a unified Django web application where hosts can create categories and clients can organize events within those categories. The platform features role-based access, background videos, PDF ticket generation, and a modern responsive design.

## Features

### Core Functionality
- **Role-Based Authentication**: Hosts create categories, clients organize events
- **Category Management**: Create, edit, delete categories with background videos
- **Event Management**: Full CRUD operations for events with detailed information
- **Ticket System**: Book tickets with PDF generation using ReportLab
- **Cash Payment**: Simplified payment confirmation system

### Technical Features
- **Background Videos**: HTML5 video backgrounds for categories (autoplay, muted, loop)
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **File Management**: Proper handling of images and videos via Django's media system
- **Admin Panel**: Comprehensive admin interface for all models
- **Security**: Input validation, CSRF protection, secure file uploads

## Installation

1. **Clone the repository**
   ```bash
   cd /Users/sarveshmodala/Desktop/HostHive
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
HostHive/
├── hosthive/           # Main project settings
├── accounts/           # User authentication and management
├── categories/         # Category management with video backgrounds
├── events/            # Event management and ticket system
├── templates/         # HTML templates
├── static/           # CSS, JS, and static images
├── media/            # User-uploaded files (videos, images)
└── requirements.txt  # Python dependencies
```

## Usage

### For Hosts
1. Register as a "Host" user type
2. Create categories with optional background videos
3. Manage your categories (edit/delete)

### For Clients
1. Register as a "Client" user type
2. Browse categories and create events within them
3. Manage your events (edit/view registrations)

### For Attendees
1. Browse events and categories
2. Book tickets for events
3. Confirm cash payment
4. Download PDF tickets

## Models

### User (Extended)
- Custom user model with `user_type` field (host/client)
- Additional fields: phone number

### Category
- Name, description, host (foreign key)
- Background video and image uploads
- Timestamps and active status

### Event
- Comprehensive event details (name, description, date, time, location)
- Category and organizer relationships
- Pricing and capacity management
- Image uploads

### Ticket
- Event registration with unique ticket numbers
- Attendee information and payment status
- PDF generation support

## Key Features Implementation

### Background Videos
- HTML5 video elements with autoplay, muted, loop
- File upload validation (50MB limit)
- Proper media serving through Django

### PDF Ticket Generation
- ReportLab integration for professional tickets
- Unique ticket numbers with UUID
- Downloadable after payment confirmation

### Responsive Design
- Bootstrap 5 framework
- Mobile-first approach
- Custom CSS with modern gradients and animations

### Security
- CSRF protection on all forms
- File upload validation
- User permission checks
- Input sanitization

## Admin Panel

Access the admin panel at `/admin/` with superuser credentials to manage:
- Users and their roles
- Categories and their content
- Events and registrations
- Ticket issuance and status

## Development Notes

- Uses SQLite for development (easily configurable for production databases)
- Media files stored in `media/` directory
- Static files in `static/` directory
- Crispy Forms for enhanced form rendering
- Bootstrap 5 for responsive UI components

## Future Enhancements

- Email notifications for event updates
- Real-time notifications
- Payment gateway integration
- Event calendar view
- Advanced search and filtering
- Social media integration

## License

This project is built for educational and demonstration purposes.