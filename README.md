# AI-QA Blog

A Django-powered blog focused on AI and Quality Assurance topics, featuring a custom editorial design system built with Tailwind CSS.

## Stack

- Python 3.9 / Django 4.2.9
- Tailwind CSS via CDN
- CKEditor 4 (rich text editing)
- WhiteNoise (static file serving)
- SQLite

## Design System

- **Primary:** Forest green `#0D3B38`
- **Accent:** Burnt amber `#C8601A`
- **Fonts:** Playfair Display (headings) + DM Sans (body)
- **Shadows:** Brand-tinted layered CSS custom properties

## Local Development

```bash
# Clone
git clone https://github.com/mmehta84/cblog.git
cd cblog

# Set up virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
python manage.py migrate

# Run
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Features

- Post creation with CKEditor rich text editor
- Categories and tags with filtered views
- Full-text search
- Reading time and view count
- Auto-generated slugs and excerpts
- Login-protected post creation/editing
- Responsive sidebar (categories, tags, recent posts)
- Animated hero with underline highlight

## Deployment (PythonAnywhere)

See WSGI config in `/var/www/enigma888_pythonanywhere_com_wsgi.py`. Set these environment variables there:

```python
os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'enigma888.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://enigma888.pythonanywhere.com'
```

Static files URL: `/static/` → `/home/enigma888/cblog/staticfiles`
Media files URL: `/media/` → `/home/enigma888/cblog/media`
