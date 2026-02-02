# 🔧 Quick Fixes Guide

> Copy-paste solutions for the most critical issues

---

## 1. Add Session Validation (5 mins)

Replace every view that uses `request.session['uid']` or `request.session['sid']`:

### Before:
```python
def favorites(request):
    uid = request.session['uid']  # ❌ Crashes if not logged in
```

### After:
```python
def favorites(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid = request.session['uid']  # ✅ Safe
```

**Apply to**: `favorites`, `add_favorite`, `remove_favorite`, `profile`, `cart`, `add_cart`, `remove_cart`, `checkout`, `orders`, `add_parts`, `parts`, `edit_part`, `delete_part`, `view_orders`, `ship_item`

---

## 2. Add Logout (2 mins)

### views.py
```python
def logout(request):
    request.session.flush()
    return redirect('/login/')
```

### urls.py
```python
path('logout/', views.logout),
```

---

## 3. Hash Passwords (10 mins)

### views.py - Registration
```python
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == "POST":
        # ... existing code ...
        password = make_password(request.POST.get("password"))  # ← Hash it
        reg = Register(name=name, email=email, phone=phone, password=password)
```

### views.py - Login
```python
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = Register.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            request.session['uid'] = user.id
            return redirect('/user/')
        
        seller = Seller.objects.filter(email=email).first()
        if seller and check_password(password, seller.password):
            if seller.rights == 'Seller':
                request.session['sid'] = seller.id
                return redirect('/seller/')
            elif seller.rights == 'New Seller':
                msg = 'New Seller'
        else:
            msg = 'Invalid'
```

⚠️ **Note**: Existing users need password reset after this change!

---

## 4. Add Stock Validation (3 mins)

### views.py - add_cart
```python
def add_cart(request, id):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login/')
    
    reg = Register.objects.get(id=uid)
    part = VehiclePart.objects.get(id=id)
    
    # ✅ Check stock
    if part.stock < 1:
        return redirect('/vehicle-parts/')  # Or show error
    
    ct = Cart.objects.filter(user=reg, part=part)
    if ct:
        ct.update(quantity=F('quantity') + 1)
    else:
        cart = Cart(user=reg, part=part)
        cart.save()
    return redirect('/cart/')
```

---

## 5. Deduct Stock on Checkout (5 mins)

### views.py - checkout
```python
def checkout(request):
    # ... existing code ...
    
    if request.method == "POST":
        # ... create order ...
        
        for i in cart:
            # ✅ Deduct stock
            i.part.stock -= i.quantity
            i.part.save()
            
            op = OrderItems(order=ord, item=i.part, quantity=i.quantity)
            op.save()
        
        cart.delete()
        return redirect('/success/')
```

---

## 6. Remove Fake Social Buttons (2 mins)

In `login.html` and `register.html`, replace social login section:

### Option A: Remove entirely
Delete the `<div class="social-login">` block

### Option B: Disable with message
```html
<div class="social-login" style="opacity: 0.5; pointer-events: none;">
    <p style="text-align: center; color: #999;">Social login coming soon!</p>
</div>
```

---

## 7. Add Email Duplicate Check (3 mins)

### views.py - register
```python
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # ✅ Check for existing email
        if Register.objects.filter(email=email).exists():
            return render(request, "register.html", {'error': 'Email already registered'})
        
        # Continue with registration...
```

### register.html - Add error display
```html
{% if error %}
<div style="color: red; text-align: center; margin-bottom: 15px;">
    {{ error }}
</div>
{% endif %}
```

---

## Checklist

- [ ] Session validation on all protected views
- [ ] Add logout view and URL
- [ ] Hash passwords (warn about existing users!)
- [ ] Stock validation on add_cart
- [ ] Stock deduction on checkout
- [ ] Remove/disable fake social buttons
- [ ] Email duplicate check on registration
