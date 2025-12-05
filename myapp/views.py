from django.shortcuts import render,redirect
from .models import *
from django.db.models import F

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        reg=Register(name=name,email=email,phone=phone,password=password)
        reg.save()
        return redirect('/login/')
    return render(request, "register.html")

def seller_register(request):
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        password=request.POST.get("password")
        reg=Seller(name=name,email=email,phone=phone,address=address,password=password)
        reg.save()
        return redirect('/login/')
    return render(request, "seller_register.html")

def login(request):
    msg=''
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        log=Register.objects.filter(email=email,password=password)
        sell=Seller.objects.filter(email=email,password=password)
        if log:
            for i in log:
                if i.rights == 'User':
                    request.session['uid']=i.id
                    return redirect('/user/')
                elif i.rights == 'Admin':
                    return redirect('/adminp/')
        elif sell:
            for i in sell:
                if i.rights=='Seller':
                    request.session['sid']=i.id
                    return redirect('/seller/')
                elif i.rights=='New Seller':
                    msg='New Seller'
        else:
            msg='Invalid'
    return render(request, "login.html",{'msg':msg})

def user(request):
    cars = Car.objects.all()
    return render(request, "user/user.html",{'cars':cars})

def admin(request):
    return render(request, "admin/admin.html")

def seller(request):
    return render(request, "seller/seller.html")

def add_car(request):
    msg=False
    if request.method == "POST":
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
        car=Car(make=make,model=model,year=year,price=price,category=category,fuel_type=fuel_type,
                description=description,engine=engine,horse_power=hpower,transmission=transmission,
                mpg_city=mpg_city,mpg_hway=mpg_hway,features=features,image=image)
        car.save()
        msg=True
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
    return render(request, "user/car-detail.html",{'car':car})

def compare(request):
    cars=Car.objects.all()
    return render(request, "user/compare.html",{'cars':cars})

def collections(request):
    cars=Car.objects.all()
    return render(request, "user/collections.html",{'cars':cars})

def add_favorite(request,id):
    car=Car.objects.get(id=id)
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    fav=Favorite.objects.filter(car=car,user=reg)
    if not fav:
        fav=Favorite(car=car,user=reg)
        fav.save()
    return redirect('/favorites/')

def favorites(request):
    uid = request.session['uid']
    reg = Register.objects.get(id=uid)
    fav=Favorite.objects.filter(user=reg)
    return render(request, "user/favorites.html",{'fav':fav})

def remove_favorite(request,id):
    Favorite.objects.filter(id=id).delete()
    return redirect('/favorites/')

def profile(request):
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        if password:
            Register.objects.filter(id=uid).update(name=name,email=email,phone=phone,password=password)
        else:
            Register.objects.filter(id=uid).update(name=name,email=email,phone=phone)
        return redirect('/profile/')
    return render(request, "user/profile.html",{'reg':reg})

def add_parts(request):
    sid=request.session['sid']
    sell=Seller.objects.get(id=sid)
    car=Car.objects.all()
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
        image=request.FILES.get("image")
        veh=Car.objects.get(id=vid)
        part=VehiclePart(seller=sell,name=name,number=number,brand=brand,category=category,price=price,stock=stock,condition=condition,description=description,vehicle=veh,image=image)
        part.save()
        return redirect('/add-parts/')
    return render(request, "seller/add-parts.html",{'car':car})

def parts(request):
    sid = request.session['sid']
    sell = Seller.objects.get(id=sid)
    parts= VehiclePart.objects.filter(seller=sell)
    return render(request, "seller/parts.html",{'parts':parts})

def edit_part(request,id):
    part=VehiclePart.objects.get(id=id)
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
        VehiclePart.objects.filter(id=id).update(name=name, number=number, brand=brand, category=category, price=price, stock=stock,
                           condition=condition, description=description, vehicle=veh)
        return redirect(f'/edit-part/{id}/')
    return render(request, "seller/edit-part.html",{'part':part})

def delete_part(request,id):
    VehiclePart.objects.filter(id=id).delete()
    return redirect('/parts/')

def vehicle_parts(request):
    parts= VehiclePart.objects.all()
    cars=Car.objects.all()
    return render(request, "user/vehicle-parts.html",{'parts':parts,'vehicles':cars})

def part_details(request,id):
    part=VehiclePart.objects.get(id=id)
    return render(request, "user/part-details.html",{'part':part})

def cart(request):
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    cart=Cart.objects.filter(user=reg)
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
    uid = request.session['uid']
    reg = Register.objects.get(id=uid)
    part=VehiclePart.objects.get(id=id)
    ct=Cart.objects.filter(user=reg,part=part)
    if ct:
        ct.update(quantity=F('quantity') + 1)
    else:
        cart=Cart(user=reg,part=part)
        cart.save()
    return redirect('/cart/')

def remove_cart(request,id):
    Cart.objects.filter(id=id).delete()
    return redirect('/cart/')

def checkout(request):
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    cart=Cart.objects.filter(user=reg)
    total = 0
    for i in cart:
        total += i.total_price
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        city=request.POST.get("city")
        state=request.POST.get("state")
        zip=request.POST.get("zip")
        country=request.POST.get("country")
        ord = Order.objects.create(user=reg, fname=fname, lname=lname, email=email, phone=phone, address=address,
                                   city=city,
                                   state=state, zip=zip, country=country)
        for i in cart:
            op=OrderItems(order=ord, item=i.part,quantity=i.quantity)
            op.save()
        cart.delete()
        return redirect('/success/')
    return render(request, "user/checkout.html",{'cart':cart,'total':total})

def success(request):
    return render(request, "user/success.html")

def orders(request):
    uid=request.session['uid']
    reg=Register.objects.get(id=uid)
    ord=Order.objects.filter(user=reg)
    return render(request, "user/orders.html",{'ord':ord})

def view_orders(request):
    ord=Order.objects.all()
    return render(request, "seller/orders.html",{'ord':ord})

def ship_item(request,id):
    Order.objects.filter(id=id).update(status='Shipped')
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