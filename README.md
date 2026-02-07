# MFU Web Portal

A comprehensive Django-based web portal for sports centers, designed to manage athletes, coaches, parents, admins, and finances through role-based access control. The platform integrates Google OAuth2 authentication, email verification, and a flexible permission system.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Running Locally](#running-locally)
- [Production Deployment](#production-deployment)
- [Environment Variables](#environment-variables)
- [API & Permissions](#api--permissions)
- [Troubleshooting](#troubleshooting)

---

## Features

✅ **Role-Based Access Control (RBAC)**
- Admin, Coach, Parent, Athlete, Finance & Inventory Manager roles
- Special privilege tags (Center Head, Head Coach)
- Granular permission system via decorators, mixins, and template tags

✅ **Authentication**
- Email-based authentication
- Google OAuth2 integration
- Email verification workflow
- Secure password reset

✅ **Dashboard Navigation**
- Dynamic tabbed navigation based on user roles
- Responsive navbar with user profile dropdown
- Permission-protected views and pages

✅ **Extensible Architecture**
- Multiple portal apps (admin, coach, parent, athlete, finance)
- Pluggable data models (events, volunteering, centers, etc.)
- Template inheritance with shared base layout

---

## Project Structure

```
MFU/
├── config/                      # Project configuration
│   ├── settings/
│   │   ├── base.py             # Common settings
│   │   ├── development.py       # Dev-specific settings
│   │   └── production.py        # Production settings
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── apps/
│   ├── core/                   # User, Role, RoleTag models & permissions
│   ├── authentication/         # Custom auth views (login, register, logout)
│   ├── profiles/               # User profile dashboard
│   ├── admin_portal/           # Admin dashboard
│   ├── coach_portal/           # Coach dashboard
│   ├── parent_portal/          # Parent dashboard
│   ├── athlete_portal/         # Athlete dashboard
│   ├── finance_portal/         # Finance & inventory dashboard
│   ├── events/                 # Events management
│   ├── volunteering/           # Volunteering management
│   └── centers/                # Center information
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar & tabs
│   ├── authentication/        # Login, register templates
│   ├── profiles/              # Profile dashboard template
│   └── ...                    # Portal-specific templates
├── static/                    # CSS, JS, images
├── media/                     # User-uploaded files
├── manage.py                  # Django management CLI
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (dev)
└── README.md                  # This file
```

---

## Prerequisites

### Required Software

- **Python 3.10+** ([download](https://www.python.org/downloads/))
- **MySQL 8.0+** ([download](https://dev.mysql.com/downloads/mysql/))
- **Git** ([download](https://git-scm.com/))
- **pip** (comes with Python)

### Recommended

- **Virtual environment tool** (venv, conda)
- **MySQL GUI** (MySQL Workbench, DBeaver, or Sequel Pro)
- **Code editor** (VS Code, PyCharm)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MFU
```

### 2. Create a Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

**Option A: Using MySQL Command Line**

```bash
mysql -u root -p
```

Then execute:
```sql
CREATE DATABASE mfu_portal;
CREATE USER 'mfu_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON mfu_portal.* TO 'mfu_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. Create new schema: `mfu_portal`
3. Create new user with credentials and grant privileges

### 5. Configure Environment Variables

Create/update the `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development)
DB_ENGINE=django.db.backends.mysql
DB_NAME=mfu_portal
DB_USER=mfu_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (Development - Console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@mfuportal.com

# Google OAuth2 (Get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Application Settings
SITE_ID=1
DJANGO_SETTINGS_MODULE=config.settings.development
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Or use the convenience script:
```bash
python create_superuser.py
```

### 8. Load Initial Data (Optional)

Seed roles and sample data:
```bash
python manage.py seed_roles
```

---

## Running Locally

### Start the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000**

### Access Key Endpoints

- **Home/Login:** http://127.0.0.1:8000/auth/login/
- **Register:** http://127.0.0.1:8000/auth/register/
- **Profile Dashboard:** http://127.0.0.1:8000/profiles/dashboard/
- **Django Admin:** http://127.0.0.1:8000/admin/
- **Permission Examples:** http://127.0.0.1:8000/core/examples/

### Debugging

Enable Django Debug Toolbar by ensuring `DEBUG=True` in `.env`:
- Debug info appears at the bottom right of pages
- SQL queries, templates, and settings are inspectable

---

## Production Deployment

### 1. Environment Setup

Update `.env` for production:

```env
# Django Settings
SECRET_KEY=your-very-secure-secret-key-generated-randomly
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (Production - MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=mfu_portal_prod
DB_USER=mfu_prod_user
DB_PASSWORD=very-secure-password-here
DB_HOST=your-mysql-host.com
DB_PORT=3306

# Email Configuration (Production - SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Google OAuth2
GOOGLE_CLIENT_ID=your-production-google-client-id
GOOGLE_CLIENT_SECRET=your-production-google-client-secret

# Application Settings
SITE_ID=1
DJANGO_SETTINGS_MODULE=config.settings.production
```

### 2. Generate Secret Key

Use Django's `get_random_secret_key()`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste into your `.env` as `SECRET_KEY`.

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This gathers all CSS, JS, and images into `staticfiles/` for serving.

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create Production Superuser

```bash
python manage.py createsuperuser
```

### 6. Deployment Options

#### Option A: Using Gunicorn + Nginx (Recommended)

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Start Gunicorn:**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Nginx Configuration Example:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/MFU/staticfiles/;
    }

    location /media/ {
        alias /path/to/MFU/media/;
    }
}
```

**Use a process manager (systemd, supervisor) to keep Gunicorn running.**

#### Option B: Using PaaS (Heroku, PythonAnywhere, Railway)

**Heroku Example:**

1. Create `Procfile` in project root:
```
web: gunicorn config.wsgi --log-file -
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Option C: Using Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t mfu-portal .
docker run -p 8000:8000 --env-file .env mfu-portal
```

### 7. Enable HTTPS

Use Let's Encrypt + Certbot:
```bash
sudo certbot certonly --nginx -d yourdomain.com
```

Update Nginx to redirect HTTP to HTTPS and serve SSL certificates.

### 8. Set Up Automated Backups

Schedule daily database backups:
```bash
0 2 * * * mysqldump -u mfu_prod_user -p'password' mfu_portal_prod > /backups/mfu_$(date +\%Y\%m\%d).sql
```

---

## Environment Variables

| Variable | Dev Value | Prod Value | Description |
|----------|-----------|-----------|-------------|
| `DEBUG` | `True` | `False` | Enable Django debug mode |
| `SECRET_KEY` | dev-key | random-secure-key | Django secret key for sessions/tokens |
| `ALLOWED_HOSTS` | localhost | yourdomain.com | Allowed hostnames |
| `DB_ENGINE` | mysql | mysql | Database backend |
| `DB_NAME` | mfu_portal | mfu_portal_prod | Database name |
| `DB_USER` | root | mfu_prod_user | Database user |
| `DB_PASSWORD` | (blank) | secure-password | Database password |
| `DB_HOST` | localhost | mysql.example.com | Database host |
| `DB_PORT` | 3306 | 3306 | Database port |
| `EMAIL_BACKEND` | console | smtp | Email delivery method |
| `EMAIL_HOST` | (none) | smtp.gmail.com | SMTP server |
| `EMAIL_HOST_USER` | (none) | your-email@gmail.com | SMTP username |
| `EMAIL_HOST_PASSWORD` | (none) | app-password | SMTP password |
| `GOOGLE_CLIENT_ID` | (blank) | your-client-id | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | (blank) | your-secret | Google OAuth client secret |
| `SITE_ID` | 1 | 1 | Django sites framework ID |
| `DJANGO_SETTINGS_MODULE` | config.settings.development | config.settings.production | Django settings module |

---

## API & Permissions

### User Roles

- **Admin** - Full system access with optional Center Head tag
- **Coach** - Manage athletes and training with optional Head Coach tag
- **Parent** - View child progress and rankings
- **Athlete** - View personal scores and training
- **Finance & Inventory Manager** - Manage finances and equipment

### Using the Permission System

**In Views (Class-Based):**
```python
from apps.core.mixins.permissions import RoleRequiredMixin
from apps.core.models import Role

class AdminDashboardView(RoleRequiredMixin, TemplateView):
    required_roles = [Role.ADMIN]
    template_name = 'admin/dashboard.html'
```

**In Views (Function-Based):**
```python
from apps.core.decorators.permissions import require_roles
from apps.core.models import Role

@require_roles([Role.ADMIN])
def admin_only_view(request):
    return render(request, 'admin/dashboard.html')
```

**In Templates:**
```django
{% load permission_tags %}

{% if request.user|has_role:'admin' %}
    <a href="/admin-portal/">Admin Dashboard</a>
{% endif %}

{% if request.user|can_manage_events %}
    <a href="/events/manage/">Manage Events</a>
{% endif %}
```

---

## Troubleshooting

### Database Connection Issues

**Error: `Access denied for user 'root'@'localhost'`**
- Verify MySQL is running: `sudo service mysql status` (Linux) or check Services (Windows)
- Check credentials in `.env`
- Reset MySQL password if needed

**Error: `No module named 'MySQLdb'`**
```bash
pip install mysqlclient
```

### Migration Issues

**Error: `No migration for app 'core'`**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading

```bash
python manage.py collectstatic --clear --noinput
```

### Permission Denied Errors

- Verify user has roles assigned in Django admin
- Check `REQUIRED_ROLES` in view class/decorator
- View [core/permission_examples.html](templates/core/permission_examples.html) for testing

### Email Not Sending

**Development (Console Backend):**
- Check console output; emails print there

**Production (SMTP):**
- Verify `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- For Gmail: use [App Passwords](https://myaccount.google.com/apppasswords), not your regular password
- Check firewall allows port 587 (SMTP)

### Debug Toolbar Not Showing

- Ensure `DEBUG=True` in `.env`
- Check `INTERNAL_IPS` in `config/settings/development.py`
- Browser request must originate from `127.0.0.1` or localhost

---

## Support & Contribution

For issues, feature requests, or contributions:
1. Create an issue in the repository
2. Fork and submit a pull request
3. Follow PEP 8 code style

---

## License

This project is part of the MFU Web Portal initiative.

---

**Last Updated:** February 6, 2026  
**Version:** 1.0.0


## Superadmin

http://127.0.0.1:8001/admin

Username: admin@mfu.com
Password: admin