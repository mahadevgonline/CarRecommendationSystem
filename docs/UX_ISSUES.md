# 🔍 UX Analysis & Issues Report

> **Project**: OnlineCarRecommendationSystem (AutoSelect)  
> **Date**: December 15, 2024  
> **Scope**: User Experience, Edge Cases, Security Issues

---

## 🔴 Critical Issues

### 1. Plaintext Password Storage
**Location**: `models.py` - `Register.password`, `Seller.password`  
**Risk**: HIGH - Complete security compromise if database is leaked

**Current Code**:
```python
password = models.CharField(max_length=100)
```

**Fix** (Medium Effort):
```python
from django.contrib.auth.hashers import make_password, check_password

# On registration
reg.password = make_password(password)

# On login
if check_password(password, stored_hash):
```

---

### 2. No Session Validation on Protected Routes
**Location**: `views.py` - All user/seller authenticated views  
**Risk**: HIGH - KeyError if user visits protected page without login

**Affected Views**:
- `favorites()`, `profile()`, `cart()`, `checkout()`, `orders()` → use `request.session['uid']`
- `add_parts()`, `parts()` → use `request.session['sid']`

**Current Behavior**: Crashes with `KeyError` if session key missing

**Fix** (Simple):
```python
def favorites(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid = request.session['uid']
    # ...
```

**Better Fix** (Medium Effort): Create authentication decorator
```python
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'uid' not in request.session:
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def favorites(request):
    # ...
```

---

### 3. No Logout Functionality
**Location**: Missing entirely  
**Impact**: Users cannot securely end their session

**Fix** (Simple):
```python
# views.py
def logout(request):
    request.session.flush()
    return redirect('/login/')

# urls.py
path('logout/', views.logout),
```

---

## 🟠 UX Edge Cases

### 4. Empty States Not Handled
**Affected Pages**:
- Collections page with 0 cars
- Favorites with 0 items
- Cart with 0 items
- Orders with 0 history
- Similar cars with 0 matches

**Current Behavior**: Empty content area, confusing for users

**Fix** (Simple - Template change):
```html
{% if cars %}
    <!-- Car grid -->
{% else %}
    <div class="empty-state">
        <i class="fas fa-car"></i>
        <h3>No cars available</h3>
        <p>Check back later for new listings!</p>
    </div>
{% endif %}
```

---

### 5. No Form Validation (Server-Side)
**Location**: `register()`, `seller_register()`, `add_car()`, `checkout()`

**Missing Validations**:
- Email format validation
- Phone number format (stored as IntegerField - can overflow)
- Password minimum length
- Password confirmation matching (only client-side)
- Required field validation

**Current Impact**: 
- Duplicate emails allowed
- Invalid phone numbers stored
- Weak passwords accepted

**Fix** (Medium Effort):
```python
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # Check duplicate email
        if Register.objects.filter(email=email).exists():
            return render(request, "register.html", {'error': 'Email already exists'})
        
        # Validate phone
        phone = request.POST.get("phone")
        if not phone.isdigit() or len(phone) < 10:
            return render(request, "register.html", {'error': 'Invalid phone'})
        
        # Continue registration...
```

---

### 6. Stock Not Validated When Adding to Cart
**Location**: `views.py:add_cart()`  
**Impact**: Users can add unlimited items even if stock is 0

**Current Code**:
```python
def add_cart(request, id):
    # No stock check!
    part = VehiclePart.objects.get(id=id)
    cart = Cart(user=reg, part=part)
    cart.save()
```

**Fix** (Simple):
```python
def add_cart(request, id):
    part = VehiclePart.objects.get(id=id)
    if part.stock < 1:
        messages.error(request, "Part out of stock!")
        return redirect('/vehicle-parts/')
    # Continue...
```

---

### 7. No Stock Deduction After Order
**Location**: `views.py:checkout()`  
**Impact**: Inventory never decrements, overselling possible

**Fix** (Simple):
```python
def checkout(request):
    # After creating order items:
    for i in cart:
        # Deduct stock
        i.part.stock -= i.quantity
        i.part.save()
        
        op = OrderItems(order=ord, item=i.part, quantity=i.quantity)
        op.save()
```

---

### 8. Car Deletion Cascades to Favorites & Parts
**Location**: `models.py` - `on_delete=models.CASCADE`  
**Impact**: Deleting a car removes all user favorites and seller parts without warning

**Recommendation**: Add soft delete or confirmation workflow

---

### 9. Social Login Buttons Non-Functional
**Location**: `login.html`, `register.html`  
**Impact**: Users click Google/Facebook buttons with no result

**Quick Fix**: Remove buttons or add "Coming Soon" label
**Long Fix**: Implement OAuth with `django-allauth`

---

### 10. No Search Functionality
**Location**: User pages (`/user/`, `/vehicle-parts/`)  
**Impact**: Users must scroll through all items to find what they need

**Fix** (Medium Effort):
```python
def user(request):
    query = request.GET.get('q', '')
    cars = Car.objects.all()
    if query:
        cars = cars.filter(
            Q(make__icontains=query) | 
            Q(model__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, "user/user.html", {'cars': cars, 'query': query})
```

---

## 🟡 Minor Issues

### 11. Phone Number as IntegerField
**Location**: `models.py` - `Register.phone`, `Seller.phone`, `Order.phone`  
**Issue**: Integer can overflow, leading zeros are lost

**Fix**: Change to CharField
```python
phone = models.CharField(max_length=20)
```

---

### 12. Hardcoded Navigation Links
**Location**: All templates - `index.html` links, nav links  
**Issue**: Links like `href="#"` and `href="index.html"` mixed with Django URLs

**Fix**: Use Django URL template tags
```html
<a href="{% url 'home' %}">Home</a>
```

---

### 13. No Pagination
**Location**: `/collections/`, `/vehicle-parts/`, `/cars/`  
**Impact**: Page loads slow with many items

**Fix** (Medium Effort):
```python
from django.core.paginator import Paginator

def collections(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 12)  # 12 per page
    page = request.GET.get('page')
    cars = paginator.get_page(page)
    return render(request, "user/collections.html", {'cars': cars})
```

---

### 14. No Error Pages
**Location**: Missing 404.html, 500.html  
**Impact**: Users see ugly default Django error pages

---

### 15. No Order Cancellation
**Location**: Missing feature  
**Impact**: Users cannot cancel orders after placing them

---

## Summary Table

| # | Issue | Severity | Effort |
|---|-------|----------|--------|
| 1 | Plaintext passwords | 🔴 Critical | Medium |
| 2 | No session validation | 🔴 Critical | Simple |
| 3 | No logout | 🔴 Critical | Simple |
| 4 | Empty states | 🟠 Medium | Simple |
| 5 | No server validation | 🟠 Medium | Medium |
| 6 | No stock check (cart) | 🟠 Medium | Simple |
| 7 | No stock deduction | 🟠 Medium | Simple |
| 8 | Cascade delete | 🟠 Medium | Medium |
| 9 | Social buttons fake | 🟡 Low | Simple/Long |
| 10 | No search | 🟡 Low | Medium |
| 11 | Phone as Integer | 🟡 Low | Simple |
| 12 | Hardcoded links | 🟡 Low | Medium |
| 13 | No pagination | 🟡 Low | Medium |
| 14 | No error pages | 🟡 Low | Simple |
| 15 | No order cancel | 🟡 Low | Medium |
