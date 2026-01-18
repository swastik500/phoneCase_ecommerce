# CaseHaven - Phone Case Store

A Django-based e-commerce platform for selling phone cases. Features user authentication, product catalog, cart, orders, payments, and admin management.

## Features
- User registration, login, and profile management
- Product catalog with detail and list views
- Shopping cart functionality
- Order checkout and history
- Payment integration (Razorpay, PayPal-ready)
- Admin dashboard for managing products and orders

## Project Structure
- `accounts/` - User authentication and profile
- `cart/` - Shopping cart logic
- `catalog/` - Product catalog
- `core/` - Home, dashboard, and shared logic
- `orders/` - Order management
- `payments/` - Payment processing
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files (excluded from repo)
- `ecommerce/` - Project settings and configuration

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phone_case_store.git
   cd phone_case_store
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your secrets.
   ```bash
   cp .env.example .env
   # Edit .env with your keys
   ```
5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the site at `http://localhost:8000/`
- Admin dashboard at `/admin/`

## Environment Variables
See `.env.example` for required variables (SECRET_KEY, payment keys, etc.). Never commit your real `.env` file.

## License
MIT

## Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

## Contact
For support, contact: admin@yourstore.com
