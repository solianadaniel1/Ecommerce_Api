# E-commerce API

This is the backend API for an E-commerce . It allows users to manage products, orders, categories, and user authentication. The project is built using Django and Django REST Framework.


## Setup Instructions

Follow these steps to set up the development environment:

1. **Create a virtual environment**:
   In your project folder, run the following command to create a virtual environment:
   ```bash
   python -m venv env

2. **Install the Django Rest Framework**:
   In your project folder, run the following command to install DRF:
   ```bash
   pip install djangorestframework 

3. **Package for Securing Data**:
   ## Secure Sensitive Data
   To keep sensitive data out of the source code, install `python-decouple`:
   ```bash
   pip install python-decouple

4. **Package for filtering**: 
   ##  Filtering of Querysets
   In your project folder, run the following command to install to allows users to filter querysets:
   ```bash
   pip install django-filter

5. **Package for Mysql**: 
   ##  Database Connector for MySQL
   In your project folder, run the following command used in Python database 
   connector to MySQL:
   ```bash
   pip install mysqlclient

6. **Package for Image Processing**: 
   ##  Processing Image Tasks such as Resizing and Conversion
   In your project folder, run the following command used to process image tasks:
   ```bash
   pip install pillow

7. **Package for PEP 8 style guide**: 
   ##  Python code against the PEP 8 style guide
   In your project folder, run the following command used to check Python code against the PEP 8 style guide :
   ```bash
   pip install pycodestyle

8. **Package Identify Potential Bugs**: 
   ##  Identify Potential Bugs in Python code
   In your project folder, run the following command used to identifying potential bugs in Python code:
   ```bash
   pip install pyflakes

9. **Create a new Django project**:
   Create a django project
   ```bash
   django-admin startproject product_api

10. **Create a new Django app**:
   Create a new Django app 
   ```bash
   python manage.py startapp product
   python manage.py startapp order
   python manage.py startapp user

11. **Add the app to project**:
   Open product_api/settings.py and add 'products' to the INSTALLED_APPS list.
   INSTALLED_APPS = [
    'rest_framework',  # Django REST Framework
    'products',  # Your app
]

12. **Run the development server**:
   Run the development server to verify the setup
   ```bash
    python manage.py runserver

## Features and Endpoints
- List all products.
- Create a new products.
- Retrieve details of a specific products.
- Update all fields of a products.
- Partially update a products (e.g., update the price).
- Delete a products.

## Product Endpoints
- GET /products/: List all products.
- POST /products/: Add a new product (admin-only).
- GET /products/<id>/: Retrieve product details.
- PUT /products/<id>/: Update product (admin-only).
- DELETE /products/<id>/: Delete product (admin-only).
## Wishlist Endpoints
- GET /wishlist/: View all wishlist items for the logged-in user.
- POST /wishlist/: Add a product to the wishlist.
- DELETE /wishlist/<id>/: Remove a product from the wishlist.
## Review Endpoints
- GET /reviews/<product_id>/: Get all reviews for a product.
- POST /reviews/: Add a review for a product.
- PUT /reviews/<id>/: Update a review.
- DELETE /reviews/<id>/: Delete a review.
## Order Endpoints
- GET /orders/: View all orders for the logged-in user.
- POST /orders/: Place a new order.
- GET /orders/<id>/: Retrieve details of a specific order.
- PUT /orders/<id>/: Update order status (admin-only).
## User Endpoints
- POST /register/: Register a new user.
- POST /login/: Login to get a JWT token.
- GET /profile/: View the user profile.

# Token Authentication Setup

This API uses token-based authentication to secure the endpoints. To access the API, users must obtain a token.

## Setup Steps

1. **Install Dependencies**: Make sure `djangorestframework` and `djangorestframework-simplejwt` are installed.
   ```bash
   pip install djangorestframework
   pip install djangorestframework-simplejwt
