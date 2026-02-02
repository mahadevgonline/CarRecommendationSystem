# 🚗 OnlineCarRecommendationSystem - Agent Context Guide

## Project Overview
**AutoSelect** - A Django-based car recommendation and vehicle parts e-commerce platform.

### Tech Stack
- **Backend**: Django 5.2.8
- **Database**: SQLite
- **Frontend**: Vanilla HTML/CSS/JS with inline styles
- **Media**: File-based uploads to `/media/images/`

---

## Architecture

### Application Structure
```
OnlineCarRecommendationSystem/
├── OnlineCarRecommendationSystem/  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myapp/                          # Main application
│   ├── models.py                   # 8 data models
│   ├── views.py                    # 30+ view functions
│   ├── urls.py                     # Route definitions
│   └── templates/
│       ├── admin/                  # Admin panel (8 templates)
│       ├── seller/                 # Seller dashboard (5 templates)
│       └── user/                   # User frontend (13 templates)
├── media/images/                   # Uploaded car/part images
└── db.sqlite3                      # Database
```

---

## Data Models

| Model | Purpose | Key Relationships |
|-------|---------|-------------------|
| `Register` | User accounts | → Favorite, Cart, Order |
| `Seller` | Seller accounts | → VehiclePart |
| `Car` | Car listings | → Favorite, VehiclePart |
| `Favorite` | User wishlists | FK: Register, Car |
| `VehiclePart` | Parts for sale | FK: Seller, Car |
| `Cart` | Shopping cart | FK: Register, VehiclePart |
| `Order` | Checkout orders | FK: Register |
| `OrderItems` | Order line items | FK: Order, VehiclePart |

---

## User Roles & Flows

### 1. User (Regular Customer)
- Browse cars at `/user/`
- View car details with similar recommendations at `/car-detail/<id>/`
- Add favorites at `/add-favorite/<id>/`
- Browse vehicle parts at `/vehicle-parts/`
- Cart management at `/cart/`
- Checkout at `/checkout/`
- View orders at `/orders/`

### 2. Seller
- **Approval Required**: New sellers must wait for admin approval
- Dashboard at `/seller/`
- Manage parts at `/parts/`, `/add-parts/`, `/edit-part/<id>/`
- View customer orders at `/view-orders/`
- Ship items at `/ship-item/<id>/`

### 3. Admin
- Dashboard at `/adminp/`
- Manage cars: `/add-car/`, `/cars/`, `/edit-car/<id>/`, `/delete-car/<id>/`
- Approve sellers: `/new-sellers/`, `/approve-seller/<id>/`
- View all sellers at `/sellers/`

---

## Session Management
```python
request.session['uid']  # User ID (Register model)
request.session['sid']  # Seller ID (Seller model)
```

---

## ⚠️ Known Issues (Updated: Dec 16, 2024)

### ✅ Fixed Security Issues
1. ~~Plaintext passwords~~ → **FIXED**: Now using Django's `make_password`/`check_password`
2. ~~No authentication middleware~~ → **FIXED**: Session validation added to all protected views
3. ~~No logout functionality~~ → **FIXED**: Logout available at `/logout/`
4. ~~No email duplicate check~~ → **FIXED**: Registration now prevents duplicate emails
5. ~~No stock validation~~ → **FIXED**: Cart prevents adding out-of-stock items
6. ~~No stock deduction~~ → **FIXED**: Checkout now decrements inventory

### ⚠️ Pending Improvements
- Social login buttons (planned for future)
- Password reset functionality for existing users
- Pagination for long lists

---

## Development Commands
```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Run tests
python manage.py test myapp
```

---

## Recent Changes
- **Similar Cars Feature**: Car detail page now shows up to 4 similar cars by category
- Located in `views.py:car_detail()` and `car-detail.html`

---

## Files to Know
- `myapp/views.py` - All business logic
- `myapp/models.py` - Database schema
- `myapp/urls.py` - URL routing
- `myapp/templates/user/` - Customer-facing templates
- `OnlineCarRecommendationSystem/settings.py` - Project configuration
