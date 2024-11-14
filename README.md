
# Django Store Project

This is a simple Django project for managing a store, including categories and products. The project allows users to view categories, products, and detailed information about specific products.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [URL Patterns](#url-patterns)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lukagoguadze2/djangoProject.git
   cd django-store-project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and go to `http://127.0.0.1:8000/` to access the application.

## Usage

This project allows users to perform the following actions:

- View all categories
- View all products
- View products in a specific category
- View detailed information about a specific product

## URL Patterns

The following URLs are defined in this project:

1. **Categories**
   - **URL**: `/categories/`
   - **View**: `views.categories`
   - **Description**: Displays a list of all categories.

2. **Products**
   - **URL**: `/products/`
   - **View**: `views.products`
   - **Description**: Displays a list of all products.

3. **Category**
   - **URL**: `/category/`
   - **View**: `views.category_html`
   - **Description**: Displays a specific category page.

4. **Category Products**
   - **URL**: `/category/<int:category_id>/products`
   - **View**: `views.category_products`
   - **Description**: Displays all products under the specified category.

5. **Product Details**
   - **URL**: `/product/<int:product_id>/details`
   - **View**: `views.product_details`
   - **Description**: Displays detailed information about a specific product.

