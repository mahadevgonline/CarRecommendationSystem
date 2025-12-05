from django.shortcuts import render,redirect
from .models import *

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

def login(request):
    msg=False
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        log=Register.objects.filter(email=email,password=password)
        if log:
            for i in log:
                if i.rights == 'User':
                    request.session['uid']=i.id
                    return redirect('/user/')
                elif i.rights == 'Admin':
                    return redirect('/adminp/')
        else:
            msg=True
    return render(request, "login.html",{'msg':msg})

def user(request):
    cars = Car.objects.all()
    return render(request, "user/user.html",{'cars':cars})

def admin(request):
    return render(request, "admin/admin.html")

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

def products(request):
    cars=Car.objects.all()
    if request.method == "POST":
        name=request.POST.get("name")
        stock=request.POST.get("stock")
        price=request.POST.get("price")
        category=request.POST.get("category")
        description=request.POST.get("description")
        suitable_car=request.POST.get("suitable_name")
        Car.objects.filter(id=id).update(name=name, stock=stock, suitable_car=suitable_car, price=price, category=category,description=description)
    return render(request, "user/products.html", {'cars': cars})

def add_product(request):
    msg = False
    if request.method == "POST":
        name=request.POST.get("name")
        stock=request.POST.get("stock")
        price=request.POST.get("price")
        category=request.POST.get("category")
        description=request.POST.get("description")
        suitable_car=request.POST.get("suitable_car")
        pro=CarParts(name=name,stock=stock,price=price,category=category,description=description,suitable_car=suitable_car)
        pro.save()
        return redirect('/add-product/')
        msg = True
    return render(request, "admin/add-product.html", {'msg': msg})
