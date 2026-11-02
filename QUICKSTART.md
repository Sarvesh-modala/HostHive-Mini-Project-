# HostHive - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Run Setup Script
```bash
./setup.sh
```

### 2. Start Development Server
```bash
source venv/bin/activate
python manage.py runserver
```

### 3. Open Your Browser
Visit: http://127.0.0.1:8000

## 🔑 Login Credentials

### Admin Panel (http://127.0.0.1:8000/admin)
- **Username:** admin
- **Password:** admin123

### Sample Users
- **Host:** host1 / password123
- **Client:** client1 / password123

## 🎯 What to Try

### As a Host (host1):
1. Login with host1/password123
2. Go to Categories → Create Category
3. Add background videos (MP4 files)
4. Manage your categories

### As a Client (client1):
1. Login with client1/password123
2. Browse categories
3. Create events in categories
4. Manage your events

### As a Visitor:
1. Browse categories and events
2. Register as host or client
3. Book tickets for events
4. Download PDF tickets

## 📁 Key Features to Explore

- **Background Videos:** Upload MP4 videos for categories
- **Event Management:** Full CRUD for events
- **Ticket System:** Book and download PDF tickets
- **Cash Payment:** Simple payment confirmation
- **Responsive Design:** Works on mobile and desktop
- **Admin Panel:** Comprehensive management interface

## 🛠️ Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Database Operations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Add Sample Data
```bash
python manage.py populate_data
```

## 📱 Mobile Testing

The application is fully responsive. Test on different screen sizes:
- Desktop: Full featured interface
- Tablet: Optimized layout
- Mobile: Touch-friendly navigation

## 🎨 Customization

### Colors & Themes
Edit `static/css/style.css` to customize:
- Primary colors
- Gradients
- Animations
- Layout spacing

### Templates
Modify templates in `templates/` directory:
- `base/` - Layout and home page
- `accounts/` - Authentication pages
- `categories/` - Category management
- `events/` - Event management

## 🔧 Configuration

### Settings
Edit `hosthive/settings.py` for:
- Database configuration
- Media/static file settings
- Email configuration (future)
- Security settings

### URLs
Main URL configuration in `hosthive/urls.py`
App-specific URLs in each app's `urls.py`

## 📊 Admin Features

Access comprehensive admin at `/admin/`:
- User management with roles
- Category management with media
- Event oversight and statistics
- Ticket tracking and status
- System-wide analytics

## 🎥 Video Upload Tips

For best performance with background videos:
- Use MP4 format
- Keep files under 50MB
- Optimize for web (H.264 codec)
- Consider video length (shorter is better)
- Test autoplay compatibility

## 🎫 PDF Ticket Features

Generated tickets include:
- Unique ticket numbers
- Event details (date, time, location)
- Attendee information
- QR codes (future enhancement)
- Professional formatting

## 🚀 Production Deployment

For production deployment:
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure media file storage
5. Add proper security settings
6. Set up email backend
7. Configure domain and SSL

## 📞 Support

For issues or questions:
1. Check the main README.md
2. Review Django documentation
3. Check model definitions in each app
4. Test with sample data first