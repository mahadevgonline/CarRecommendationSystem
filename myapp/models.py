from django.db import models

class Register(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=100)
    rights=models.CharField(max_length=100,default='User')
    def __str__(self):
        return self.name

class Seller(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    rights=models.CharField(max_length=100,default='New Seller')
    def __str__(self):
        return self.name

class Car(models.Model):
    make=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    year=models.IntegerField()
    price=models.IntegerField()
    category=models.CharField(max_length=100)
    fuel_type=models.CharField(max_length=100)
    description=models.TextField()
    engine=models.CharField(max_length=100)
    horse_power=models.IntegerField()
    transmission=models.CharField(max_length=100)
    mpg_city=models.CharField(max_length=100)
    mpg_hway=models.CharField(max_length=100)
    features=models.JSONField()
    image=models.ImageField(upload_to="images/")
    def __str__(self):
        return self.make

class Favorite(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    car=models.ForeignKey(Car,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name

class VehiclePart(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100)
    number=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    price=models.IntegerField()
    stock=models.IntegerField()
    condition=models.CharField(max_length=100)
    vehicle=models.ForeignKey(Car,on_delete=models.CASCADE)
    description=models.TextField()
    image=models.ImageField(upload_to="images/")
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    part=models.ForeignKey(VehiclePart,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return self.user.name
    @property
    def total_price(self):
        return self.quantity * self.part.price

class Order(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=100,default='Processing',null=True)
    payment_method=models.CharField(max_length=100,default='COD')
    def __str__(self):
        return self.user.name

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    item=models.ForeignKey(VehiclePart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    @property
    def total_price(self):
        return self.quantity * self.item.price

class Notification(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='notifications')
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications')
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.seller.name} - Order #{self.order.id}"