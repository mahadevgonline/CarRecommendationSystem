from django.db import models

class Register(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=100)
    rights=models.CharField(max_length=100,default='User')
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

class CarParts(models.Model):
    name = models.CharField(max_length=100)
    stock = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    suitable_car = models.CharField(max_length=100, default="All Cars")
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name
