# E-commerce Bookstore API

This is the backend API for an E-commerce bookstore. It allows users to manage books, categories, and user authentication. The project is built using Django and Django REST Framework.


## Setup Instructions

Follow these steps to set up the development environment:

1. **Create a virtual environment**:
   In your project folder, run the following command to create a virtual environment:
   ```bash
   python -m venv venv

2. **Install the Django Rest Framework**:
   In your project folder, run the following command to install DRF:
   ```bash
   pip install django djangorestframework 

3. **Create a new Django project**:
   Create a django project
   ```bash
   django-admin startproject bookstore_api

4. **Create a new Django app**:
   Create a new Django app (for handling books and categories)
   ```bash
  python manage.py startapp books

4. **Add the app to project**:
   Open bookstore_api/settings.py and add 'books' to the INSTALLED_APPS list.
   INSTALLED_APPS = [
    # Other default apps...
    'rest_framework',  # Django REST Framework
    'books',  # Your app
]

4. **Run the development server**:
   Run the development server to verify the setup
   ```bash
    python manage.py runserver

## Features
- List all books.
- Create a new book.
- Retrieve details of a specific book.
- Update all fields of a book.
- Partially update a book (e.g., update the price).
- Delete a book.

# Token Authentication Setup

This API uses token-based authentication to secure the endpoints. To access the API, users must obtain a token.

## Setup Steps

1. **Install Dependencies**: Make sure `djangorestframework` and `djangorestframework-simplejwt` are installed.
   ```bash
   pip install djangorestframework
   pip install djangorestframework-simplejwt
