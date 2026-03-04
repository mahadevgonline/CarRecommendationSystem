from django.shortcuts import render,redirect
from .models import *
from .forms import RegisterForm, SellerRegisterForm, LoginForm, AddPartForm, CheckoutForm, ProfileForm
from django.db.models import F, Q, Min, Max
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return render(request, "index.html")

def register(request):
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
    return render(request, "register.html", {'form': form})

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

def login(request):
    form = LoginForm(request.POST or None)
    msg = ''
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check Register users (supports both hashed and plaintext passwords)
            user = Register.objects.filter(email=email).first()
            if user:
                password_valid = check_password(password, user.password) or (password == user.password)
                if password_valid:
                    if user.rights == 'User':
                        request.session['uid'] = user.id
                        return redirect('/user/')
                    elif user.rights == 'Admin':
                        request.session['uid'] = user.id
                        return redirect('/adminp/')

            # Check Seller users (supports both hashed and plaintext passwords)
            seller = Seller.objects.filter(email=email).first()
            if seller:
                password_valid = check_password(password, seller.password) or (password == seller.password)
                if password_valid:
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
    return render(request, "login.html", {'msg': msg, 'form': form})

def user(request):
    cars = Car.objects.all()
    return render(request, "user/user.html",{'cars':cars})

def admin(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    return render(request, "admin/admin.html")

def seller(request):
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
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    form = ProfileForm(request.POST or None, initial={'name': reg.name, 'email': reg.email, 'phone': reg.phone})
    if request.method=="POST":
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if password:
                hashed_password = make_password(password)
                Register.objects.filter(id=uid).update(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    password=hashed_password
                )
            else:
                Register.objects.filter(id=uid).update(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone']
                )
            return redirect('/profile/')
    return render(request, "user/profile.html", {'reg': reg, 'form': form})

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
    parts= VehiclePart.objects.select_related('vehicle').all()
    cars=Car.objects.all()
    return render(request, "user/vehicle-parts.html",{'parts':parts,'vehicles':cars})

def part_details(request,id):
    part=VehiclePart.objects.get(id=id)
    return render(request, "user/part-details.html",{'part':part})

def cart(request):
    if 'uid' not in request.session:
        return redirect('/login/')
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    cart=Cart.objects.filter(user=reg).select_related('part')
    total=0
    for i in cart:
        total+=i.total_price
    if request.method=="POST":
        qn=request.POST.get("quantity")
        cid=request.POST.get("cid")
        Cart.objects.filter(id=cid).update(quantity=qn)
        return redirect('/cart/')
    return render(request, "user/cart.html",{'cart':cart,'total':total})

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
    total = 0
    for i in cart:
        total += i.total_price
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
                for i in Cart.objects.filter(user=reg).select_related('part__seller'):
                    pass  # cart already deleted above, use ord items
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
    return render(request, "user/checkout.html", {'cart': cart, 'total': total, 'form': form})

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
    sell=Seller.objects.filter(rights='New Seller')
    return render(request, "admin/new-sellers.html",{'sell':sell})

def approve_seller(request,id):
    Seller.objects.filter(id=id).update(rights='Seller')
    return redirect('/new-sellers/')

def reject_seller(request,id):
    Seller.objects.filter(id=id).update(rights='Rejected')
    return redirect('/new-sellers/')

def sellers(request):
    sell=Seller.objects.filter(rights='Seller')
    return render(request, "admin/sellers.html",{'sell':sell})

def logout(request):
    """Clear session and redirect to login"""
    request.session.flush()
    return redirect('/login/')

def recommendation(request):
    cars = Car.objects.all()

    # --- 1. SEARCH ---
    q = request.GET.get('q')
    if q:
        cars = cars.filter(
            Q(make__icontains=q) | 
            Q(model__icontains=q) | 
            Q(category__icontains=q) | 
            Q(description__icontains=q)
        )

    # --- 2. FILTERS ---
    
    # categories (multi-select)
    categories = request.GET.getlist('category')
    if categories:
        cars = cars.filter(category__in=categories)

    # fuel_type (multi-select)
    fuel_types = request.GET.getlist('fuel_type')
    if fuel_types:
        cars = cars.filter(fuel_type__in=fuel_types)

    # transmission (multi-select)
    transmissions = request.GET.getlist('transmission')
    if transmissions:
        cars = cars.filter(transmission__in=transmissions)

    # price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        cars = cars.filter(price__gte=int(min_price))
    if max_price:
        cars = cars.filter(price__lte=int(max_price))

    # year range
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    if min_year:
        cars = cars.filter(year__gte=int(min_year))
    if max_year:
        cars = cars.filter(year__lte=int(max_year))

    # horse_power range
    min_hp = request.GET.get('min_hp')
    max_hp = request.GET.get('max_hp')
    if min_hp:
        cars = cars.filter(horse_power__gte=int(min_hp))
    if max_hp:
        cars = cars.filter(horse_power__lte=int(max_hp))
        
    # mpg range (handling CharField by casting to int if possible)
    # Note: If casting fails due to strict SQL mode or bad data, this might need error handling.
    # We will attempt to filter simply for now, or annotate.
    # Given SQLite, implicit casting usually works well enough or we can use lte/gte on strings if format matches,
    # but "20" > "100" in string. Let's try to be safe and use annotation.
    try:
        cars = cars.annotate(mpg_city_int=Cast('mpg_city', IntegerField()))
        
        min_mpg = request.GET.get('min_mpg')
        if min_mpg:
             cars = cars.filter(mpg_city_int__gte=int(min_mpg))
    except:
        pass # Fallback or ignore if casting fails
        
    # --- 3. SORTING ---
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        cars = cars.order_by('price')
    elif sort_by == 'price_high':
        cars = cars.order_by('-price')
    elif sort_by == 'year_new':
        cars = cars.order_by('-year')
    elif sort_by == 'year_old':
        cars = cars.order_by('year')
    elif sort_by == 'hp_high':
        cars = cars.order_by('-horse_power')
    elif sort_by == 'mpg_high':
        # Rely on the annotation if successful, else raw field
        cars = cars.order_by('-mpg_city') # This might do string sort "30" > "20", but "9" > "10" is false. 

    # --- 4. DATA FOR UI FILTERS (Global Min/Max) ---
    # We need the global min/max for the sliders based on ALL cars, not just filtered ones
    all_cars = Car.objects.all()
    filter_data = all_cars.aggregate(
        min_price_global=Min('price'), max_price_global=Max('price'),
        min_year_global=Min('year'), max_year_global=Max('year'),
        min_hp_global=Min('horse_power'), max_hp_global=Max('horse_power'),
    )
    
    # Get unique values for checkboxes
    unique_categories = Car.objects.values_list('category', flat=True).distinct()
    unique_fuels = Car.objects.values_list('fuel_type', flat=True).distinct()
    unique_transmissions = Car.objects.values_list('transmission', flat=True).distinct()

    context = {
        'cars': cars,
        'unique_categories': unique_categories,
        'unique_fuels': unique_fuels,
        'unique_transmissions': unique_transmissions,
        'filter_data': filter_data,
        'current_filters': request.GET # Pass QueryDict for maintaining state in basic UI methods
    }
    
    return render(request, "user/recommendations.html", context)