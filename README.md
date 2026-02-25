# 🍕 FoodHub - Full Stack Restaurant Website

A modern, responsive restaurant management and food delivery system built with Django. Order food online, track deliveries, make table reservations, and manage everything from a powerful admin dashboard.

## ✨ Features

### 🛍️ Customer Features
- **User Authentication**: Secure registration, login/logout, user profiles
- **Browse Menu**: Categorized food items with images and descriptions
- **Search Functionality**: Find food items quickly by name or category
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout System**: Detailed order summary before payment
- **Payment Integration**: 
  - Razorpay (UPI, Card, Net Banking, Google Pay, PhonePe)
  - Cash on Delivery option
- **Order Tracking**: Real-time order status tracking
- **Table Booking**: Reserve tables with date/time selection
- **Order History**: View all past orders and reservations
- **Contact Form**: Send messages to restaurant

### 🎛️ Admin Features
- **Admin Dashboard**: Complete restaurant management system
- **Menu Management**: Add, edit, delete food items
- **Order Management**: View, update, and track all orders
- **Payment Records**: Track all payments and transactions
- **Table Reservations**: Manage table bookings
- **User Management**: View and manage customers
- **Analytics**: Sales reports, popular items, revenue tracking
- **Restaurant Info**: Configure restaurant details and working hours

### 🎨 User Interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI**: Bootstrap 5 with custom animations
- **Smooth Interactions**: Hover effects, transitions, loading states
- **Accessibility**: Semantic HTML, proper form labels
- **SEO Optimized**: Meta tags, proper heading hierarchy

## 📦 Tech Stack

**Backend:**
- Python 3.10+
- Django 6.0
- SQLite3 (development) / PostgreSQL (production)
- Razorpay API for payment processing

**Frontend:**
- HTML5
- CSS3 (with animations and gradients)
- Bootstrap 5
- JavaScript (vanilla JS, no jQuery)
- FontAwesome Icons

**Database:**
- SQLite (default)
- Easily configured for PostgreSQL

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual Environment

### Installation

1. **Clone or Extract the Project**
```bash
cd Hotel/Respro
```

2. **Create Virtual Environment** (if not already created)
```bash
python -m venv myenv
```

3. **Activate Virtual Environment**
```bash
# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate
```

4. **Install Dependencies**
```bash
pip install django pillow razorpay
```

5. **Run Migrations**
```bash
python manage.py migrate
```

6. **Create Superuser** (if not already created)
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@foodhub.com
# Password: admin123
```

7. **Start Development Server**
```bash
python manage.py runserver
```

8. **Access the Application**
- Website: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## 📱 Project Structure

```
Respro/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
│
├── Respro/                  # Main project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── accounts/               # User authentication app
│   ├── models.py          # User-related models
│   ├── views.py           # Authentication views
│   ├── urls.py            # Auth URLs
│   └── admin.py
│
├── menu/                  # Food menu management
│   ├── models.py          # Category, FoodItem
│   ├── views.py           # Menu display views
│   ├── urls.py            # Menu URLs
│   └── admin.py
│
├── cart/                  # Shopping cart
│   ├── models.py          # Cart, CartItem
│   ├── views.py           # Cart operations
│   ├── urls.py            # Cart URLs
│   └── admin.py
│
├── orders/                # Order management
│   ├── models.py          # Order, OrderItem
│   ├── views.py           # Order views
│   ├── urls.py            # Order URLs
│   └── admin.py
│
├── payments/              # Payment processing
│   ├── models.py          # Payment model
│   ├── views.py           # Razorpay integration
│   ├── urls.py            # Payment URLs
│   └── admin.py
│
├── booking/               # Table reservations
│   ├── models.py          # Reservation model
│   ├── views.py           # Booking views
│   ├── urls.py            # Booking URLs
│   └── admin.py
│
├── dashboard/             # Admin dashboard
│   ├── models.py          # Dashboard models
│   ├── views.py           # Admin views
│   ├── urls.py            # Dashboard URLs
│   └── admin.py
│
├── Base_app/              # Core app
│   ├── models.py          # ContactMessage, RestaurantInfo
│   ├── views.py
│   ├── admin.py
│   └── migrations/
│
├── Template/              # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── register.html     # Registration
│   ├── login.html        # Login
│   ├── menu.html         # Menu display
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout
│   ├── payment.html      # Payment options
│   ├── book_table.html   # Table booking
│   ├── my_orders.html    # User orders
│   ├── my_reservations.html # User reservations
│   ├── profile.html      # User profile
│   └── ...
│
├── Static/               # Static files (CSS, JS, Images)
└── Media/                # User uploaded files (food images)
```

## 🔐 User Roles

### Customer
- Default user role
- Can browse menu, order food, make payments, book tables
- Access to personal dashboard (orders, profile)

### Admin
- Full access to dashboard
- Manage food items, orders, payments, reservations
- View analytics and reports
- Note: Create admin user with `createsuperuser` command

## 💳 Payment Integration

### Razorpay Setup

1. **Get Razorpay API Keys**
   - Sign up at https://razorpay.com
   - Get your TEST/LIVE API keys from dashboard

2. **Update Settings**
   - Open `Respro/settings.py`
   - Update these values:
   ```python
   RAZORPAY_KEY_ID = 'your_key_id_here'
   RAZORPAY_KEY_SECRET = 'your_key_secret_here'
   ```

3. **Install Razorpay SDK**
   ```bash
   pip install razorpay
   ```

4. **Test Payment**
   - Use Razorpay test credentials
   - Test card: 4111 1111 1111 1111
   - Any future date and any CVV

### Cash on Delivery
- Available without any setup
- Order will be marked as pending payment until collected

## 🗄️ Database Models

### User (Django Built-in)
- username, email, password, first_name, last_name

### Category
- name, description

### FoodItem
- name, category (FK), description, price, image, available, created_at

### Cart
- user (OneToOne), created_at, updated_at
- Methods: get_total(), get_item_count()

### CartItem
- cart (FK), food_item (FK), quantity, added_at

### Order
- user, order_number, total_price
- status, payment_status, payment_method
- delivery_address, phone, special_instructions
- created_at, estimated_delivery

### OrderItem
- order, food_item, quantity, price (snapshot)

### Payment  
- user, order, amount, status
- razorpay_order_id, razorpay_payment_id, razorpay_signature
- transaction_id, payment_method

### Reservation
- user, name, email, phone
- reservation_date, reservation_time, number_of_guests
- special_requests, status

## 🎯 Key Functionality

### User Authentication
```python
# Registration
POST /register/ -> Create new user
# Login
POST /login/ -> Authenticate user
# Logout
POST /logout/ -> End session
# Profile
GET /profile/ -> View user info
```

### Menu Management
```python
# View all items
GET /menu/ -> Display menu

# Filter by category
GET /menu/category/<id>/ -> Filter items

# Search
GET /menu/search/?q=query -> Search items
```

### Shopping Cart
```python
# View cart
GET /cart/ -> Show cart contents

# Add to cart
POST /cart/add/<item_id>/ -> Add item

# Update quantity
POST /cart/update/<item_id>/ -> Change qty

# Remove item
POST /cart/remove/<item_id>/ -> Delete item

# Clear cart
POST /cart/clear/ -> Empty cart
```

### Order Management
```python
# Create order
POST /orders/create/ -> Checkout

# View orders
GET /orders/ -> My orders

# Order details
GET /orders/<order_number>/ -> Single order

# Cancel order
POST /orders/<order_number>/cancel/ -> Cancel
```

### Payment
```python
# Checkout
GET /payment/checkout/<order_number>/ -> Payment page

# Process
POST /payment/process/ -> Send to Razorpay

# Verify
POST /payment/verify/ -> Verify signature

# Success
GET /payment/success/ -> Confirmation
```

## 📊 Admin Dashboard

### Statistics
- Total orders
- Total revenue
- Number of users
- Pending orders
- Weekly orders

### Management Sections
1. **Food Items**
   - Add new items
   - Edit existing items
   - Delete items
   - Manage categories

2. **Orders**
   - View all orders
   - Update order status
   - Track deliveries
   - Cancel orders

3. **Payments**
   - View payment records
   - Check Razorpay transactions
   - Payment status tracking

4. **Reservations**
   - Manage table bookings
   - Confirm/cancel reservations
   - View guest details

5. **Analytics**
   - Revenue charts
   - Popular items
   - Order statistics
   - Time-based reports

## 🔒 Security Features

- CSRF Protection (Django built-in)
- Password hashing with Django's authentication
- SQL injection prevention (Django ORM)
- XSS protection (Django templates)
- HTTPS ready for production
- Admin login required for sensitive operations

## 🌐 Deployment

### For Production:

1. **Update Settings**
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = 'generate-new-strong-key'
```

2. **Collect Static Files**
```bash
python manage.py collectstatic
```

3. **Use PostgreSQL**
```bash
pip install psycopg2-binary
```

4. **Deploy with Gunicorn**
```bash
pip install gunicorn
gunicorn Respro.wsgi:application --bind 0.0.0.0:8000
```

5. **Use Nginx as Reverse Proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

## 📝 Testing

### Test Accounts
- **Admin**: username: `admin`, password: `admin123`
- **Test Customer**: Create via registration page

### Test Payment
- Use Razorpay test mode credentials
- Test card: 4111 1111 1111 1111
- Future expiry date, any CVV

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Missing Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Pillow Not Installed
```bash
pip install Pillow
```

## 📧 Contact Support

- Email: support@foodhub.com
- Phone: +91-XXXXXXXXXX
- Address: 123, Food Street, Restaurant City, 123456

## 📄 License

This project is for educational purposes. Feel free to modify and use as needed.

## 🙌 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [Razorpay Integration](https://razorpay.com/docs/api/)
- [SQLite for Django](https://docs.djangoproject.com/en/stable/ref/settings/#databases)

---

Made with ❤️ for Food Lovers
Happy Coding! 🚀
