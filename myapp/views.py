from django.shortcuts import render,redirect
from .models import *
from .forms import RegisterForm, SellerRegisterForm, LoginForm, AddPartForm, CheckoutForm, ProfileForm, validate_password
from django.db.models import F, Q, Min, Max, Count, Sum
import json
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
import random
import datetime
import urllib.parse

def index(request):
    return render(request, "index.html")

@never_cache
def register(request):
    # Already logged in → push them to their dashboard
    if 'uid' in request.session:
        return redirect('/user/')
    if 'sid' in request.session:
        return redirect('/seller/')
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            if Register.objects.filter(email=email).exists():
                form.add_error('email', 'Email already registered')
                return render(request, "register.html", {'form': form})
            hashed_password = make_password(form.cleaned_data['password'])
            reg = Register(
                name=form.cleaned_data['name'],
                email=email,
                phone=form.cleaned_data['phone'],
                password=hashed_password
            )
            reg.save()
            return redirect('/login/')
    response = render(request, "register.html", {'form': form})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response

def seller_register(request):
    form = SellerRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            if Seller.objects.filter(email=email).exists():
                form.add_error('email', 'Email already registered')
                return render(request, "seller_register.html", {'form': form})
            hashed_password = make_password(form.cleaned_data['password'])
            reg = Seller(
                name=form.cleaned_data['name'],
                email=email,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                password=hashed_password
            )
            reg.save()
            return redirect('/login/')
    return render(request, "seller_register.html", {'form': form})

@never_cache
def login(request):
    # Already logged in → push them to their dashboard
    if 'uid' in request.session:
        return redirect('/user/')
    if 'sid' in request.session:
        return redirect('/seller/')
    form = LoginForm(request.POST or None)
    msg = ''
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check Register users (supports both hashed and plaintext passwords)
            user = Register.objects.filter(email=email).first()
            if user:
                # SECURE: only use Django's hashed password check — no plaintext fallback
                if check_password(password, user.password):
                    if user.rights == 'User':
                        request.session['uid'] = user.id
                        return redirect('/user/')
                    elif user.rights == 'Admin':
                        request.session['uid'] = user.id
                        return redirect('/adminp/')

            # Check Seller users
            seller = Seller.objects.filter(email=email).first()
            if seller:
                if check_password(password, seller.password):
                    if seller.rights == 'Seller':
                        request.session['sid'] = seller.id
                        return redirect('/seller/')
                    elif seller.rights == 'New Seller':
                        msg = 'New Seller'
                else:
                    msg = 'Invalid'
            else:
                if not user:
                    msg = 'Invalid'
        else:
            msg = 'Invalid'
    response = render(request, "login.html", {'msg': msg, 'form': form})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response


@never_cache
def forgot_password(request):
    """Step 1: User enters email → OTP sent to that email."""
    message = None
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = Register.objects.filter(email=email).first()
        if user:
            # Generate a strict 6-digit OTP, zero-padded if necessary
            otp = str(random.randrange(1000000)).zfill(6)
            expiry = timezone.now() + datetime.timedelta(minutes=10)
            Register.objects.filter(id=user.id).update(
                otp=otp,
                otp_expiry=expiry
            )
            send_mail(
                subject='ClassicAuto — Password Reset OTP',
                message=(
                    f'Hi {user.name},\n\n'
                    f'Your one-time password (OTP) to reset your ClassicAuto password is:\n\n'
                    f'    {otp}\n\n'
                    f'This OTP is valid for 10 minutes. Do not share it with anyone.\n\n'
                    f'If you did not request this, please ignore this email.\n\n'
                    f'— ClassicAuto Team'
                ),
                from_email='noreply@classicauto.com',
                recipient_list=[email],
                fail_silently=False,
            )
        # Always show "sent" message — never reveal if email exists
        message = 'sent'
        # Encode email in URL so OTP verify page knows which user to look up
        encoded_email = urllib.parse.quote(email)
        return redirect(f'/verify-otp/?e={encoded_email}')
    return render(request, 'forgot-password.html', {'message': message, 'error': error})


@never_cache
def verify_otp(request):
    """Step 2: User enters the 6-digit OTP they received."""
    encoded_email = request.GET.get('e', '')
    email = urllib.parse.unquote(encoded_email)
    error = None

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        email = request.POST.get('email', '').strip()
        now = timezone.now()
        user = Register.objects.filter(
            email=email,
            otp=otp_entered,
            otp_expiry__gt=now
        ).first()
        if user:
            # OTP correct — go to set new password page
            encoded_email = urllib.parse.quote(email)
            return redirect(f'/reset-password/?e={encoded_email}&otp={otp_entered}')
        else:
            error = 'Invalid or expired OTP. Please try again.'

    return render(request, 'verify-otp.html', {'email': email, 'error': error})


@never_cache
def reset_password(request):
    """Step 3: User sets a new password after OTP is verified."""
    encoded_email = request.GET.get('e', '')
    otp = request.GET.get('otp', '')
    email = urllib.parse.unquote(encoded_email)
    error = None

    # Validate OTP is still valid before showing the form
    now = timezone.now()
    user = Register.objects.filter(
        email=email,
        otp=otp,
        otp_expiry__gt=now
    ).first()

    if not user:
        return render(request, 'reset-password.html', {'invalid': True})

    if request.method == 'POST':
        new_password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if new_password != confirm_password:
            error = 'Passwords do not match.'
        else:
            # Run through our password validator
            pw_error = validate_password(new_password)
            if pw_error:
                error = pw_error

        if not error:
            hashed = make_password(new_password)
            Register.objects.filter(id=user.id).update(
                password=hashed,
                otp=None,
                otp_expiry=None
            )
            return render(request, 'reset-password.html', {'success': True})

    return render(request, 'reset-password.html', {
        'email': encoded_email,
        'otp': otp,
        'error': error
    })

def user(request):
    """User homepage — displays all cars for browsing."""
    if 'uid' not in request.session:
        return redirect('/login/')
    cars = Car.objects.all()
    return render(request, "user/user.html", {'cars': cars})

def admin(request):
    if 'uid' not in request.session:
        return redirect('/login/')

    # ── Stat Cards ──────────────────────────────────────────────────────────
    total_users    = Register.objects.filter(rights='User').count()
    total_cars     = Car.objects.count()
    total_orders   = Order.objects.count()
    total_sellers  = Seller.objects.filter(rights='Seller').count()
    pending_sellers = Seller.objects.filter(rights='New Seller').count()
    total_parts    = VehiclePart.objects.count()

    # Revenue = sum of (quantity * item.price) across all OrderItems
    revenue_data   = OrderItems.objects.aggregate(
        total=Sum(F('quantity') * F('item__price'))
    )
    total_revenue  = revenue_data['total'] or 0

    # ── Recent Activity ──────────────────────────────────────────────────────
    recent_orders  = Order.objects.select_related('user').order_by('-id')[:5]
    recent_users   = Register.objects.filter(rights='User').order_by('-id')[:5]

    # ── Chart Data ───────────────────────────────────────────────────────────
    # Cars by category  →  for doughnut chart
    cars_by_cat    = list(
        Car.objects.values('category').annotate(count=Count('id')).order_by('-count')
    )
    chart_cat_labels = json.dumps([c['category'] for c in cars_by_cat])
    chart_cat_data   = json.dumps([c['count']    for c in cars_by_cat])

    # Orders by status  →  for bar chart
    orders_by_status = list(
        Order.objects.values('status').annotate(count=Count('id')).order_by('status')
    )
    chart_status_labels = json.dumps([o['status'] for o in orders_by_status])
    chart_status_data   = json.dumps([o['count']  for o in orders_by_status])

    # ── Top Cars (by favourite count) ────────────────────────────────────────
    top_cars = (
        Car.objects
        .annotate(fav_count=Count('favorite'))
        .order_by('-fav_count')[:8]
    )

    context = {
        'total_users':       total_users,
        'total_cars':        total_cars,
        'total_orders':      total_orders,
        'total_revenue':     total_revenue,
        'total_sellers':     total_sellers,
        'pending_sellers':   pending_sellers,
        'total_parts':       total_parts,
        'recent_orders':     recent_orders,
        'recent_users':      recent_users,
        'top_cars':          top_cars,
        'chart_cat_labels':  chart_cat_labels,
        'chart_cat_data':    chart_cat_data,
        'chart_status_labels': chart_status_labels,
        'chart_status_data':   chart_status_data,
    }
    return render(request, "admin/admin.html", context)


def seller(request):
    """Seller dashboard — requires seller authentication."""
    if 'sid' not in request.session:
        return redirect('/login/')
    return render(request, "seller/seller.html")

def add_car(request):
    if 'uid' not in request.session:
        return redirect('/login/')
        
    msg=False
    if request.method == "POST":
        try:
            make=request.POST.get("make")
            model=request.POST.get("model")
            year=request.POST.get("year")
            price=request.POST.get("price")
            category=request.POST.get("category")
            fuel_type=request.POST.get("fuel_type")
            description=request.POST.get("description")
            engine=request.POST.get("engine")
            hpower=request.POST.get("hpower")
            transmission=request.POST.get("transmission")
            mpg_city=request.POST.get("mpg_city")
            mpg_hway=request.POST.get("mpg_hway")
            features=request.POST.getlist("features")
            image=request.FILES['image']
            
            # Safe conversion with default values
            price = int(float(price)) if price else 0
            year = int(float(year)) if year else 0
            hpower = int(float(hpower)) if hpower else 0
            
            car=Car(make=make,model=model,year=year,price=price,category=category,fuel_type=fuel_type,
                    description=description,engine=engine,horse_power=hpower,transmission=transmission,
                    mpg_city=mpg_city,mpg_hway=mpg_hway,features=features,image=image)
            car.save()
            msg=True
        except Exception as e:
            print(f"Error adding car: {e}")
            msg = "Error"
    return render(request, "admin/add-car.html",{'msg':msg})

def cars(request):
    cars=Car.objects.all()
    return render(request, "admin/cars.html",{'cars':cars})

def view_car(request,id):
    return render(request, "admin/view-car.html",{'car':Car.objects.get(id=id)})

def edit_car(request,id):
    car=Car.objects.get(id=id)
    msg=False
    if request.method=="POST":
        make=request.POST.get("make")
        model=request.POST.get("model")
        year=request.POST.get("year")
        price=request.POST.get("price")
        category=request.POST.get("category")
        fuel_type=request.POST.get("fuel_type")
        description=request.POST.get("description")
        engine=request.POST.get("engine")
        hpower=request.POST.get("hpower")
        transmission=request.POST.get("transmission")
        mpg_city=request.POST.get("mpg_city")
        mpg_hway=request.POST.get("mpg_hway")
        Car.objects.filter(id=id).update(make=make,model=model,year=year,price=price,category=category,
                                         fuel_type=fuel_type,description=description,engine=engine,
                                         horse_power=hpower,transmission=transmission,mpg_city=mpg_city,
                                         mpg_hway=mpg_hway)
        return redirect(f'/edit-car/{id}/')
    return render(request, "admin/edit-car.html",{'car':car,'msg':msg})

def update_car_image(request,id):
    if 'uid' not in request.session:
        return redirect('/login/')
    if request.method == "POST":
        image = request.FILES.get('image')
        if image:
            car = Car.objects.get(id=id)
            car.image = image
            car.save()
    return redirect(f'/view-car/{id}/')

def delete_car(request,id):
    Car.objects.filter(id=id).delete()
    return redirect('/cars/')

def car_detail(request,id):
    car=Car.objects.get(id=id)
    similar_cars = Car.objects.filter(category=car.category).exclude(id=id)[:4]
    return render(request, "user/car-detail.html",{'car':car, 'similar_cars': similar_cars})

def compare(request):
    cars=Car.objects.all()
    return render(request, "user/compare.html",{'cars':cars})

def collections(request):
    cars=Car.objects.all()
    return render(request, "user/collections.html",{'cars':cars})

def add_favorite(request,id):
    if 'uid' not in request.session:
        return redirect('/login/')
    car=Car.objects.get(id=id)
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    fav=Favorite.objects.filter(car=car,user=reg)
    if not fav:
        fav=Favorite(car=car,user=reg)
        fav.save()
    return redirect('/favorites/')

def favorites(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid = request.session['uid']
    reg = Register.objects.get(id=uid)
    fav=Favorite.objects.filter(user=reg)
    return render(request, "user/favorites.html",{'fav':fav})

def remove_favorite(request,id):
    if 'uid' not in request.session:
        return redirect('/login/')
    Favorite.objects.filter(id=id).delete()
    return redirect('/favorites/')

def profile(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid = request.session['uid']
    reg = Register.objects.get(id=uid)
    if request.method == "POST":
        reg.name  = request.POST.get('name', reg.name).strip()
        reg.email = request.POST.get('email', reg.email).strip()
        reg.phone = request.POST.get('phone', reg.phone)
        image = request.FILES.get('profile_image')
        if image:
            reg.profile_image = image
        reg.save()
        return redirect('/profile/')
    return render(request, "user/profile.html", {'reg': reg})

def add_parts(request):
    if 'sid' not in request.session:
        return redirect('/login/')
    sid=request.session['sid']
    sell=Seller.objects.get(id=sid)
    car=Car.objects.all()
    form = AddPartForm(request.POST or None, request.FILES or None)
    if request.method=="POST":
        if form.is_valid():
            veh = Car.objects.get(id=form.cleaned_data['vehicle'])
            image = request.FILES.get("image")
            part = VehiclePart(
                seller=sell,
                name=form.cleaned_data['name'],
                number=form.cleaned_data['number'],
                brand=form.cleaned_data['brand'],
                category=form.cleaned_data['category'],
                price=form.cleaned_data['price'],
                stock=form.cleaned_data['stock'],
                condition=form.cleaned_data['condition'],
                description=form.cleaned_data['description'],
                vehicle=veh,
                image=image
            )
            part.save()
            return redirect('/add-parts/')
    return render(request, "seller/add-parts.html", {'car': car, 'form': form})

def parts(request):
    if 'sid' not in request.session:
        return redirect('/login/')
    sid = request.session['sid']
    sell = Seller.objects.get(id=sid)
    parts= VehiclePart.objects.filter(seller=sell)
    return render(request, "seller/parts.html",{'parts':parts})

def edit_part(request,id):
    if 'sid' not in request.session:
        return redirect('/login/')
    part=VehiclePart.objects.filter(id=id, seller_id=request.session['sid']).first()
    if not part:
        return redirect('/parts/')  # Or show a 403 Forbidden error
    if request.method=="POST":
        name=request.POST.get("name")
        number=request.POST.get("number")
        brand=request.POST.get("brand")
        category=request.POST.get("category")
        price=request.POST.get("price")
        stock=request.POST.get("stock")
        condition=request.POST.get("condition")
        vid=request.POST.get("vehicle")
        description=request.POST.get("description")
        veh = Car.objects.get(id=vid)
        VehiclePart.objects.filter(id=id, seller_id=request.session['sid']).update(name=name, number=number, brand=brand, category=category, price=price, stock=stock,
                           condition=condition, description=description, vehicle=veh)
        return redirect(f'/edit-part/{id}/')
    return render(request, "seller/edit-part.html",{'part':part})

def delete_part(request,id):
    if 'sid' not in request.session:
        return redirect('/login/')
    VehiclePart.objects.filter(id=id, seller_id=request.session['sid']).delete()
    return redirect('/parts/')

def vehicle_parts(request):
    parts = VehiclePart.objects.select_related('vehicle', 'seller').all()
    cars = Car.objects.all()

    # Build a list of categories with their counts for the template
    category_counts = {}
    for p in parts:
        cat = p.category if p.category else 'Other'
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # List of dicts: [{name: 'Engine Parts', key: 'engine parts', count: 5}, ...]
    categories_with_counts = [
        {'name': cat, 'key': cat.lower(), 'count': count}
        for cat, count in category_counts.items()
    ]

    return render(request, "user/vehicle-parts.html", {
        'parts': parts,
        'vehicles': cars,
        'categories_with_counts': categories_with_counts,
    })

def part_details(request, id):
    try:
        part = VehiclePart.objects.select_related('vehicle', 'seller').get(id=id)
    except VehiclePart.DoesNotExist:
        return HttpResponse("Part not found", status=404)

    # Compatible cars (same category, different primary vehicle)
    compatible_car_ids = (
        VehiclePart.objects
        .filter(category=part.category)
        .exclude(vehicle_id=part.vehicle_id)
        .values_list('vehicle_id', flat=True)
        .distinct()
    )
    compatible_cars = Car.objects.filter(id__in=compatible_car_ids)

    # Related parts – same category, exclude current part
    related_parts = (
        VehiclePart.objects
        .filter(category=part.category)
        .exclude(id=id)
        .select_related('vehicle')[:6]
    )

    # Reviews & rating
    reviews = part.reviews.all()[:10]
    total_reviews = part.reviews.count()
    avg_rating = 0
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    if total_reviews:
        all_reviews = list(part.reviews.all())
        avg_rating = round(sum(r.rating for r in all_reviews) / total_reviews, 1)
        for r in all_reviews:
            rating_dist[r.rating] = rating_dist.get(r.rating, 0) + 1

    # Check if user already requested notify
    user_email = request.session.get('email', '')
    already_notified = False
    if user_email and part.stock == 0:
        already_notified = PartNotifyRequest.objects.filter(part=part, email=user_email).exists()

    return render(request, "user/part-details.html", {
        'part': part,
        'compatible_cars': compatible_cars,
        'related_parts': related_parts,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_dist': rating_dist,
        'already_notified': already_notified,
        'user_email': user_email,
    })


def cart(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    cart=Cart.objects.filter(user=reg).select_related('part')
    subtotal=0
    for i in cart:
        subtotal+=i.total_price
    
    promo_success = None
    promo_error = None
    if request.method=="POST":
        if "promo_code" in request.POST:
            code = request.POST.get("promo_code").strip().upper()
            if "20" in code:
                request.session['promo'] = "VINTAGE20"
                promo_success = f"Code '{code}' applied! 20% discount."
            else:
                request.session.pop('promo', None)
                if code:
                    promo_error = "Invalid promo code."
                else:
                    promo_success = "Promo code removed."
        else:
            qn=request.POST.get("quantity")
            cid=request.POST.get("cid")
            Cart.objects.filter(id=cid).update(quantity=qn)
            return redirect('/cart/')
            
    discount = 0
    if request.session.get('promo') == 'VINTAGE20':
        discount = subtotal * 0.20
        
    total = subtotal - discount
    return render(request, "user/cart.html",{'cart':cart,'subtotal':subtotal,'discount':discount,'total':total,'promo_success':promo_success,'promo_error':promo_error})

def add_cart(request,id):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid = request.session['uid']
    reg = Register.objects.get(id=uid)
    part=VehiclePart.objects.get(id=id)
    # Check stock before adding
    if part.stock < 1:
        return redirect('/vehicle-parts/')
    ct=Cart.objects.filter(user=reg,part=part)
    if ct:
        ct.update(quantity=F('quantity') + 1)
    else:
        cart=Cart(user=reg,part=part)
        cart.save()
    return redirect('/cart/')

def remove_cart(request,id):
    if 'uid' not in request.session:
        return redirect('/login/')
    Cart.objects.filter(id=id, user_id=request.session['uid']).delete()
    return redirect('/cart/')

def checkout(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    cart=Cart.objects.filter(user=reg).select_related('part')
    if not cart.exists():
        return redirect('/cart/')
    total = 0
    for i in cart:
        total += i.total_price
        
    subtotal = total
    discount = 0
    if request.session.get('promo') == 'VINTAGE20':
        discount = subtotal * 0.20
    
    total = subtotal - discount
    form = CheckoutForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            with transaction.atomic():
                ord = Order.objects.create(
                    user=reg,
                    fname=form.cleaned_data['fname'],
                    lname=form.cleaned_data['lname'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zip=form.cleaned_data['zip'],
                    country=form.cleaned_data['country']
                )
                for i in cart:
                    VehiclePart.objects.filter(id=i.part.id).update(stock=F('stock') - i.quantity)
                    op=OrderItems(order=ord, item=i.part, quantity=i.quantity)
                    op.save()
                cart.delete()
                # Send a notification to each relevant seller
                sellers_notified = set()
                for op_item in OrderItems.objects.filter(order=ord).select_related('item__seller'):
                    seller_obj = op_item.item.seller
                    if seller_obj and seller_obj.id not in sellers_notified:
                        sellers_notified.add(seller_obj.id)
                        Notification.objects.create(
                            seller=seller_obj,
                            order=ord,
                            message=f"New order #{ord.id} received from {reg.name}. Please review and accept."
                        )
            return redirect('/success/')
    return render(request, "user/checkout.html", {'cart': cart, 'subtotal': subtotal, 'discount': discount, 'total': total, 'form': form})

def success(request):
    return render(request, "user/success.html")

def orders(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    ord=Order.objects.filter(user=reg).prefetch_related('orderitems_set__item')
    return render(request, "user/orders.html",{'ord':ord})

def manage_orders(request):
    if 'sid' not in request.session:
        return redirect('/login/')
    
    sid = request.session['sid']
    try:
        seller = Seller.objects.get(id=sid)
        # STRICT FILTER: Only show orders that contain items from this seller
        # distinct() avoids duplicate rows if order has multiple items from same seller
        orders = Order.objects.filter(orderitems__item__seller=seller).distinct().order_by('-date').prefetch_related('orderitems_set__item')
        # Unread notifications for this seller
        notifications = Notification.objects.filter(seller=seller, is_read=False).order_by('-created_at')
        notif_count = notifications.count()
        return render(request, "seller/orders.html", {'ord': orders, 'notifications': notifications, 'notif_count': notif_count})
    except Seller.DoesNotExist:
        return redirect('/login/')

def update_order_status(request, id):
    if 'sid' not in request.session:
        return redirect('/login/')
    
    sid = request.session['sid']
    if request.method == "POST":
        new_status = request.POST.get('status')
        try:
            seller = Seller.objects.get(id=sid)
            # SECURITY: ensure seller owns at least one item in this order
            order = Order.objects.filter(id=id, orderitems__item__seller=seller).first()
            
            if order:
                current_status = order.status
                # Full status transition map
                transitions = {
                    'Processing':       ['Accepted', 'Rejected'],
                    'Accepted':         ['Packed'],
                    'Packed':           ['Shipped'],
                    'Shipped':          ['Out for Delivery'],
                    'Out for Delivery': ['Delivered'],
                }
                allowed_next = transitions.get(current_status, [])
                if new_status in allowed_next:
                    order.status = new_status
                    order.save()
            
        except Exception as e:
            print(f"Error updating order: {e}")
            
    return redirect('/view-orders/')


def mark_notification_read(request, id):
    if 'sid' not in request.session:
        return redirect('/login/')
    Notification.objects.filter(id=id, seller_id=request.session['sid']).update(is_read=True)
    return redirect('/view-orders/')


def new_sellers(request):
    """Admin view — list sellers awaiting approval."""
    if 'uid' not in request.session:
        return redirect('/login/')
    sell = Seller.objects.filter(rights='New Seller')
    return render(request, "admin/new-sellers.html",{'sell':sell})

def approve_seller(request, id):
    """Admin action — approve a pending seller."""
    if 'uid' not in request.session:
        return redirect('/login/')
    Seller.objects.filter(id=id).update(rights='Seller')
    return redirect('/new-sellers/')

def reject_seller(request, id):
    """Admin action — reject a pending seller."""
    if 'uid' not in request.session:
        return redirect('/login/')
    Seller.objects.filter(id=id).update(rights='Rejected')
    return redirect('/new-sellers/')

def sellers(request):
    """Admin view — list all approved sellers."""
    if 'uid' not in request.session:
        return redirect('/login/')
    sell = Seller.objects.filter(rights='Seller')
    return render(request, "admin/sellers.html",{'sell':sell})

@never_cache
def logout(request):
    """Clear session and redirect to login"""
    request.session.flush()
    response = redirect('/login/')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response





# ─────────────────────────────────────────────────────────────────
#  NOTIFY ME (AJAX POST, out-of-stock parts)
# ─────────────────────────────────────────────────────────────────
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import re as _re

@require_POST
def notify_part(request, id):
    try:
        part = VehiclePart.objects.select_related('seller').get(id=id)
    except VehiclePart.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Part not found'}, status=404)

    if part.stock > 0:
        return JsonResponse({'ok': False, 'error': 'Part is already in stock'})

    email = request.POST.get('email', '').strip().lower()

    # Validate email format
    if not _re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return JsonResponse({'ok': False, 'error': 'Please enter a valid email address'})

    # Prevent duplicates (race-condition-safe)
    obj, created = PartNotifyRequest.objects.get_or_create(part=part, email=email)

    if not created:
        return JsonResponse({'ok': True, 'already': True,
                             'message': "You're already on the notification list for this part!"})

    # Email seller about the demand
    try:
        if part.seller and part.seller.email:
            send_mail(
                subject=f'📦 Restock Demand: {part.name}',
                message=(
                    f'Hi {part.seller.name},\n\n'
                    f'A customer ({email}) has requested to be notified when '
                    f'"{part.name}" (Part #{part.number}) is back in stock.\n\n'
                    f'This part currently has 0 units in stock. Consider restocking!\n\n'
                    f'— ClassicAuto Marketplace'
                ),
                from_email=None,
                recipient_list=[part.seller.email],
                fail_silently=True,
            )
    except Exception:
        pass

    return JsonResponse({'ok': True, 'already': False,
                         'message': "Got it! We'll notify you the moment this part is back in stock."})


# ─────────────────────────────────────────────────────────────────
#  SUBMIT REVIEW
# ─────────────────────────────────────────────────────────────────
from django.utils.html import strip_tags

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

@require_POST
def submit_review(request, id):
    try:
        part = VehiclePart.objects.get(id=id)
    except VehiclePart.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Part not found'}, status=404)

    user_name = strip_tags(request.POST.get('user_name', '').strip())[:100]
    user_email = request.POST.get('user_email', '').strip().lower()
    comment = strip_tags(request.POST.get('comment', '').strip())

    # Validate rating
    try:
        rating = int(request.POST.get('rating', 0))
        if not 1 <= rating <= 5:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({'ok': False, 'error': 'Rating must be between 1 and 5'})

    # Validate email
    if not _re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', user_email):
        return JsonResponse({'ok': False, 'error': 'Please enter a valid email address'})

    if not user_name:
        return JsonResponse({'ok': False, 'error': 'Name is required'})
    if not comment:
        return JsonResponse({'ok': False, 'error': 'Comment is required'})

    # Check duplicate
    if PartReview.objects.filter(part=part, user_email=user_email).exists():
        return JsonResponse({'ok': False, 'error': 'You have already reviewed this part.'})

    # Handle image upload
    image_file = request.FILES.get('image')
    if image_file:
        if image_file.content_type not in ALLOWED_IMAGE_TYPES:
            return JsonResponse({'ok': False, 'error': 'Only JPG, PNG, and WebP images are allowed'})
        if image_file.size > MAX_IMAGE_SIZE:
            return JsonResponse({'ok': False, 'error': 'Image must be smaller than 2MB'})

    review = PartReview(
        part=part,
        user_name=user_name,
        user_email=user_email,
        rating=rating,
        comment=comment,
    )
    if image_file:
        review.image = image_file
    review.save()

    image_url = review.image.url if review.image else ''
    return JsonResponse({
        'ok': True,
        'review': {
            'user_name': review.user_name,
            'rating': review.rating,
            'comment': review.comment,
            'image_url': image_url,
            'created_at': review.created_at.strftime('%b %d, %Y'),
        }
    })


# ─────────────────────────────────────────────────────────────────
#  SELLER UNAVAILABLE (funny page)
# ─────────────────────────────────────────────────────────────────
def seller_unavailable(request):
    seller_id = request.GET.get('seller', '')
    part_id = request.GET.get('part', '')
    return render(request, "user/seller-unavailable.html", {
        'seller_id': seller_id,
        'part_id': part_id,
    })


# ─────────────────────────────────────────────────────────────────
#  QR CODE — generate a QR image (cached in memory)
# ─────────────────────────────────────────────────────────────────
import qrcode
import io
import socket

_qr_cache = {}   # simple in-process cache

def _get_lan_ip():
    """Return the machine's LAN IP so QR codes work across devices on the same WiFi."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def part_qr(request, id):
    try:
        part = VehiclePart.objects.get(id=id)
    except VehiclePart.DoesNotExist:
        return HttpResponse("Part not found", status=404)

    uid = request.GET.get('u', '')
    cache_key = f"{id}_{part.price}_{uid}"
    
    if cache_key not in _qr_cache:
        port = request.META.get('SERVER_PORT', '8000')
        lan_ip = _get_lan_ip()
        
        uid_param = f"?u={uid}" if uid else ""
        payment_url = f'http://{lan_ip}:{port}/part-payment/{id}/{uid_param}'

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=3,
        )
        qr.add_data(payment_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color='#3e2723', back_color='#f5f1e6')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        _qr_cache[cache_key] = buf.getvalue()

    return HttpResponse(_qr_cache[cache_key], content_type='image/png')


# ─────────────────────────────────────────────────────────────────
#  QR PAYMENT INFO PAGE (opened when QR is scanned)
# ─────────────────────────────────────────────────────────────────
def part_payment_info(request, id):
    # If opened from a phone scanning the QR code, adopt the session
    u = request.GET.get('u')
    if u:
        request.session['uid'] = u
        
    try:
        part = VehiclePart.objects.select_related('vehicle', 'seller').get(id=id)
    except VehiclePart.DoesNotExist:
        return HttpResponse("Part not found", status=404)

    port = request.META.get('SERVER_PORT', '8000')
    lan_ip = _get_lan_ip()
    
    uid = request.session.get('uid', '')
    uid_param = f"?u={uid}" if uid else ""
    qr_url = f'/part-qr/{id}/{uid_param}'
    pay_url = f'http://{lan_ip}:{port}/part-payment-success/{id}/'

    return render(request, "user/part-payment.html", {
        'part': part,
        'qr_url': qr_url,
        'pay_url': pay_url,
        'lan_ip': lan_ip,
        'port': port,
    })


# ─────────────────────────────────────────────────────────────────
#  PAYMENT SUCCESS PAGE
# ─────────────────────────────────────────────────────────────────
def part_payment_success(request, id):
    try:
        part = VehiclePart.objects.select_related('vehicle', 'seller').get(id=id)
    except VehiclePart.DoesNotExist:
        return HttpResponse("Part not found", status=404)
        
    uid = request.session.get('uid')
    order = None
    guest = True
    session_key = f'qr_paid_{id}'
    
    if uid:
        try:
            reg = Register.objects.get(id=uid)
            guest = False
            
            # Prevent duplicate orders if user refreshes the success page
            if not request.session.get(session_key):
                from django.db import transaction
                with transaction.atomic():
                    order = Order.objects.create(
                        user=reg,
                        fname=reg.name.split()[0] if reg.name else 'Buyer',
                        lname=reg.name.split()[-1] if len(reg.name.split()) > 1 else '',
                        email=reg.email,
                        phone=reg.phone,
                        address='Digital / QR Payment',
                        city='-', state='-', zip='-', country='-',
                        payment_method='QR/UPI',
                        status='Processing'
                    )
                    OrderItems.objects.create(order=order, item=part, quantity=1)
                    
                    if part.stock > 0:
                        part.stock -= 1
                        part.save()
                        
                    if part.seller:
                        Notification.objects.create(
                            seller=part.seller,
                            order=order,
                            message=f"New QR payment order #{order.id} received for {part.name}. Please review."
                        )
                request.session[session_key] = order.id
            else:
                # Retrieve the already-created order if they just refreshed
                order_id = request.session.get(session_key)
                order = Order.objects.filter(id=order_id).first()
                
        except Register.DoesNotExist:
            guest = True

    return render(request, "user/payment-success.html", {
        'part': part, 
        'order': order, 
        'guest': guest
    })


# ─────────────────────────────────────────────────────────────────
#  AI CAR FINDER — Gemini-powered recommendations
# ─────────────────────────────────────────────────────────────────
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from django.conf import settings

def ai_car_finder(request):
    """Render the AI Car Finder page."""
    return render(request, "user/ai-car-finder.html")


@require_POST
def ai_car_recommend(request):
    """AJAX endpoint: send user query to Gemini, return car recommendations as JSON."""
    import json as _json

    if genai is None:
        return JsonResponse({'ok': False, 'error': 'Gemini AI library is not installed in this environment.'})

    query = request.POST.get('query', '').strip()
    if not query:
        return JsonResponse({'ok': False, 'error': 'Please describe what kind of car you are looking for.'})

    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return JsonResponse({'ok': False, 'error': 'Gemini API key is not configured. Please add your key in settings.py.'})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')

        prompt = f"""You are an expert automotive advisor. A user is looking for car recommendations.

User's request: "{query}"

Based on this request, recommend exactly 5 cars from anywhere in the world that best match their needs.

Return ONLY a valid JSON array of 5 objects (no markdown, no code fences, no explanation text). Each object must have these exact keys:
- "make": string (manufacturer name)
- "model": string (model name)
- "year_range": string (e.g. "2020-2024")
- "price_min": integer (estimated minimum price in USD)
- "price_max": integer (estimated maximum price in USD)
- "horsepower": integer (approximate hp)
- "engine": string (e.g. "2.0L Turbo I4", "5.0L V8", "Electric")
- "transmission": string (e.g. "Automatic", "Manual", "CVT", "Dual-Clutch")
- "fuel_type": string (e.g. "Gasoline", "Diesel", "Electric", "Hybrid")
- "body_type": string (e.g. "Sedan", "SUV", "Sports Car", "Truck", "Hatchback", "Coupe")
- "mpg": string (e.g. "25 city / 32 hwy" or "N/A" for electric)
- "top_speed": string (e.g. "155 mph")
- "zero_to_sixty": string (e.g. "5.2 seconds")
- "drivetrain": string (e.g. "AWD", "RWD", "FWD", "4WD")
- "why_recommended": string (2-3 sentence explanation of why this car matches the user's needs)
- "pros": array of 3 strings (key advantages)
- "cons": array of 2 strings (potential drawbacks)
- "match_score": integer (1-100, how well it matches the request)

Sort by match_score descending. Return ONLY the JSON array, nothing else."""

        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Clean up the response — remove markdown code fences if present
        if raw_text.startswith('```'):
            # Remove ```json or ``` at start and ``` at end
            lines = raw_text.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            raw_text = '\n'.join(lines)

        cars_data = _json.loads(raw_text)

        # Cross-reference with our database
        for car in cars_data:
            car['in_database'] = False
            car['db_id'] = None
            car['parts'] = []

            # Try to find this car in our database (fuzzy match on make + model)
            db_match = Car.objects.filter(
                Q(make__icontains=car.get('make', '')) &
                Q(model__icontains=car.get('model', ''))
            ).first()

            if db_match:
                car['in_database'] = True
                car['db_id'] = db_match.id
                car['db_price'] = db_match.price
                car['db_image'] = db_match.image.url if db_match.image else None

                # Find parts available for this car
                parts_qs = VehiclePart.objects.filter(
                    vehicle=db_match, stock__gt=0
                ).select_related('seller')[:6]
                car['parts'] = [
                    {
                        'id': p.id,
                        'name': p.name,
                        'brand': p.brand,
                        'price': p.price,
                        'category': p.category,
                        'image': p.image.url if p.image else None,
                    }
                    for p in parts_qs
                ]

        return JsonResponse({'ok': True, 'cars': cars_data})

    except _json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'AI returned an invalid response format. Please try again.'})
    except Exception as e:
        error_str = str(e)
        if '429' in error_str or 'Quota exceeded' in error_str:
            return JsonResponse({'ok': False, 'error': 'The AI service is currently very busy. Please wait about 30-60 seconds and try again!'})
        return JsonResponse({'ok': False, 'error': f'An error occurred: {error_str}'})
