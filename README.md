# Django Blog Project

A full-featured blog application built with Django, featuring user authentication, post management, comments, categories, tags, and user profiles.

## Project Overview

This is a comprehensive blog platform that allows users to:

- **Create and manage blog posts** with rich content, images, categories, and tags
- **Comment on posts** and engage with the community
- **Manage user profiles** with bio, profile pictures, and personal information
- **Browse content** by categories, tags, authors, and search functionality
- **Authenticate securely** with registration, login, logout, and password reset

## Key Features

### Content Management
- Create, edit, and delete blog posts
- Draft and published post status
- Image uploads for posts and profiles
- Category and tag organization
- View counter tracking

### User Features
- User registration and authentication
- Password reset functionality
- User profiles with customizable information
- "My Posts" section for managing personal content
- Comment system for post engagement

### Advanced Features
- Custom Django ORM managers and querysets
- Advanced filtering (by category, tag, author, popularity)
- Full-text search functionality
- Responsive design with modern UI

## Technology Stack

- **Backend**: Django 5.2.8
- **Database**: MySQL
- **Image Processing**: Pillow
- **Frontend**: HTML, CSS, Bootstrap

## Project Structure

```
Blog_project/
├── Blog_project/          # Project settings
│   ├── settings.py        # Django configuration
│   └── urls.py            # Main URL routing
├── blog/                  # Blog application
│   ├── models.py         # Database models (Post, Category, Tag, Comment, UserProfile)
│   ├── views.py          # View functions and classes
│   ├── forms.py          # Form classes
│   ├── urls.py           # Blog URL patterns
│   ├── admin.py          # Admin configuration
│   └── templates/        # HTML templates
├── media/                 # User-uploaded files
└── manage.py             # Django management script
```

## Database Models

- **Post**: Blog posts with title, content, images, categories, tags, and status
- **Category**: Post categorization
- **Tag**: Post tagging system
- **Comment**: User comments on posts
- **UserProfile**: Extended user profile information

## Quick Start

1. Install dependencies:
   ```bash
   pipenv install
   # or
   pip install -r requirements.txt
   ```

2. Configure database in `Blog_project/settings.py`

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`
