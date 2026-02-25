# 🚀 FoodHub - Installation & Setup Guide

## Step-by-Step Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Windows/Mac/Linux Operating System

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.10+
```

### Step 2: Navigate to Project Directory

```bash
cd "c:\Users\Admin\OneDrive\Desktop\Hotel\Respro"
```

### Step 3: Create Virtual Environment (If Needed)

```bash
python -m venv myenv
```

### Step 4: Activate Virtual Environment

**Windows:**
```bash
myenv\Scripts\activate
```

**macOS/Linux:**
```bash
source myenv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install Django==6.0.2
pip install Pillow==12.1.1
pip install razorpay==1.4.3
```

### Step 6: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

When prompted, enter:
- **Username**: admin
- **Email**: admin@foodhub.com
- **Password**: admin123 (or your preferred password)

### Step 8: Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 9: Access the Website

Open your browser and visit:

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🎯 First Time Setup Tasks

### 1. Create Sample Food Items

1. Go to Admin Panel: http://127.0.0.1:8000/admin/
2. Login with your superuser credentials (admin/admin123)
3. Click on "Categories" and create some categories:
   - Pizzas
   - Burgers
   - Desserts
   - Beverages

4. Click on "Food Items" and add items to each category:
   - Name: Pizza Margherita
   - Category: Pizzas
   - Price: 249
   - Description: Classic Italian pizza with fresh basil
   - Upload an image

### 2. Configure Restaurant Settings

1. Go to Admin Panel > Restaurant Info
2. Fill in your restaurant details:
   - Name: Your Restaurant Name
   - Email: restaurant@example.com
   - Phone: Your contact number
   - Address: Restaurant location
   - Opening & Closing Times

### 3. Setup Razorpay (Payment Gateway)

**Option A: Use Test Credentials (For Development)**
1. Visit https://razorpay.com
2. Create a free account and login to dashboard
3. Go to Settings > API Keys
4. Copy your TEST key ID and secret
5. Update `Respro/settings.py`:

```python
RAZORPAY_KEY_ID = 'rzp_test_xxxxxxxxxxxxx'  # Your test key
RAZORPAY_KEY_SECRET = 'xxxxxxxxxxxxxxxx'    # Your test secret
```

**Option B: Use Cash on Delivery (No Setup Required)**
- Customers can select "Cash on Delivery" during checkout
- No additional configuration needed

### 4. Test Account Creation

1. Go to http://127.0.0.1:8000/register/
2. Create a test customer account:
   - Username: testuser
   - Email: test@example.com
   - Password: test123

3. Login with your test account

### 5. Test the Full Flow

1. **Browse Menu**: Go to `/menu/` and browse food items
2. **Add to Cart**: Add items to your cart
3. **View Cart**: Check your shopping cart
4. **Checkout**: Enter delivery details
5. **Payment**: Choose payment method
   - For Razorpay: Use test card 4111 1111 1111 1111
   - For Cash on Delivery: Select COD
6. **Order Success**: View order confirmation

---

## 📱 Default Logins

### Admin Account
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: admin
- **Password**: admin123

### Dashboard (Admin)
- **URL**: http://127.0.0.1:8000/dashboard/
- **Requires**: Admin/Staff account login

---

## 🔧 Configuration Files

### `Respro/settings.py` - Main Settings

```python
# Database Settings (Default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For PostgreSQL (Production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'foodhub_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Razorpay Settings
RAZORPAY_KEY_ID = 'YOUR_KEY_ID'
RAZORPAY_KEY_SECRET = 'YOUR_KEY_SECRET'

# Email Settings (Development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email Settings (Production - Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

---

## 🌐 Project Structure Overview

```
Respro/
├── manage.py           # Django CLI
├── db.sqlite3          # SQLite Database
├── requirements.txt    # Python dependencies
├── README.md          # Main documentation
│
├── Respro/             # Main Django project
│   ├── settings.py     # Configuration
│   ├── urls.py         # URL routing
│   └── wsgi.py         # WSGI config
│
├── accounts/           # User authentication
├── menu/              # Food menu
├── cart/              # Shopping cart
├── orders/            # Order management
├── payments/          # Payment processing
├── booking/           # Table reservations
├── dashboard/         # Admin dashboard
├── Base_app/          # Core functionality
│
├── Template/          # HTML templates
│   ├── base.html      # Base template
│   ├── home.html      # Homepage
│   ├── menu.html      # Menu display
│   ├── cart.html      # Shopping cart
│   ├── checkout.html  # Checkout
│   ├── payment.html   # Payment page
│   └── ...
│
├── Static/            # CSS, JS, Images
└── Media/             # User uploads (food images)
```

---

## ✨ Key Features Tour

### For Customers

1. **Registration & Login**
   - Create account with email
   - Secure password hashing
   - Profile management

2. **Browse Menu**
   - View all food items
   - Filter by category
   - Search by name or description
   - See item images and prices

3. **Shopping Cart**
   - Add multiple items
   - Update quantities
   - View cart summary
   - Clear cart

4. **Checkout**
   - Enter delivery address
   - Special instructions
   - Order review

5. **Payment**
   - Razorpay integration (UPI, Cards, etc.)
   - Cash on Delivery option
   - Payment confirmation

6. **Order Tracking**
   - View order status
   - Estimated delivery time
   - Order history

7. **Table Booking**
   - Reserve tables
   - Select date & time
   - Special requests
   - Manage reservations

### For Admin

1. **Dashboard**
   - View statistics
   - Recent orders
   - Quick management tools

2. **Menu Management**
   - Add food items
   - Edit items
   - Delete items
   - Manage categories

3. **Order Management**
   - View all orders
   - Update order status
   - Filter by status
   - Payment tracking

4. **Table Reservations**
   - View all reservations
   - Manage bookings
   - Track guest details

5. **Analytics**
   - Revenue reports
   - Popular items
   - Order statistics
   - Time-based analytics

6. **User Management**
   - View all customers
   - Track user information
   - Manage active users

---

## 🧪 Test Cases

### Test Case 1: Customer Registration
1. Go to /register/
2. Fill form with unique username and email
3. Click Register
4. Verify success message
5. Login with new account

### Test Case 2: Browse Menu
1. Go to /menu/
2. Click category filter
3. Use search function
4. Verify items display

### Test Case 3: Add to Cart
1. Go to /menu/
2. Click "Add" button on food item
3. Verify item added to cart
4. Check cart shows correct quantity

### Test Case 4: Place Order
1. Go to cart
2. Click "Proceed to Checkout"
3. Enter delivery address
4. Select payment method
5. Verify order creation

### Test Case 5: Payment (Razorpay)
1. Select Razorpay payment
2. Click "Pay Now"
3. Use test card: 4111 1111 1111 1111
4. Enter any future date and CVV
5. Verify payment success page

### Test Case 6: Admin Dashboard
1. Login with admin account
2. Go to /dashboard/
3. View statistics
4. Add new food item
5. Manage orders
6. Check analytics

---

## 🐛 Troubleshooting

### **Port Already in Use**
```bash
# Use different port
python manage.py runserver 8001
```

### **Database Errors**
```bash
# Reset database
python manage.py migrate --run-syncdb

# Or delete and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### **Missing Migrations**
```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### **Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Image Upload Issues**
```bash
# Install Pillow
pip install Pillow

# Check media folder exists
mkdir -p Media
```

### **Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput
```

---

## 📚 Useful Django Commands

```bash
# Create a new app
python manage.py startapp appname

# Make migrations for changes
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Collect static files (production)
python manage.py collectstatic

# Flush database (reset all data)
python manage.py flush

# Check for problems
python manage.py check
```

---

## 🔐 Security Checklist

- [ ] Change default admin username/password
- [ ] Update SECRET_KEY in settings.py
- [ ] Set DEBUG = False for production
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup HTTPS/SSL certificates
- [ ] Use environment variables for sensitive data
- [ ] Configure email backend for notifications
- [ ] Setup database backups
- [ ] Use PostgreSQL for production (not SQLite)
- [ ] Setup proper logging

---

## 📖 Learning Resources

- [Django Official Docs](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Razorpay Integration Guide](https://razorpay.com/docs/api/)
- [Python Virtual Environment](https://python.readthedocs.io/en/latest/library/venv.html)

---

## 🆘 Need Help?

If you encounter any issues:

1. Check the error message carefully
2. Review the troubleshooting section
3. Check Django logs
4. Review database migrations
5. Try resetting the database
6. Check Python version compatibility

---

## 🎉 You're All Set!

The FoodHub application is now ready to use. Start adding food items, creating orders, and managing your restaurant!

**Happy Coding!** 🚀

---

*Last Updated: February 2026*
