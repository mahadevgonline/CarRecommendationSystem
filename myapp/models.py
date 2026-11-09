from django.db import models


class Register(models.Model):
    """User account for customers and admins."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    rights = models.CharField(max_length=100, default='User')
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    """Seller account requiring admin approval before listing parts."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=128)
    rights = models.CharField(max_length=100, default='New Seller')

    def __str__(self):
        return self.name


class Car(models.Model):
    """Vehicle listing in the recommendation database."""
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)
    description = models.TextField()
    engine = models.CharField(max_length=100)
    horse_power = models.IntegerField()
    transmission = models.CharField(max_length=100)
    mpg_city = models.CharField(max_length=100)
    mpg_hway = models.CharField(max_length=100)
    features = models.JSONField()
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Favorite(models.Model):
    """User's wishlisted/favourite car."""
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.name} — {self.car}"


class VehiclePart(models.Model):
    """Aftermarket or OEM part listed by a seller."""
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    condition = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Shopping cart entry linking a user to a vehicle part."""
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    part = models.ForeignKey(VehiclePart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.name} — {self.part.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.part.price


class Order(models.Model):
    """Completed checkout order."""
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, default='Processing', null=True)
    payment_method = models.CharField(max_length=100, default='COD')

    def __str__(self):
        return f"Order #{self.id} — {self.user.name}"


class OrderItems(models.Model):
    """Individual line item within an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(VehiclePart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.item.price


class Notification(models.Model):
    """Notification sent to a seller when an order is placed."""
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='notifications')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.seller.name} — Order #{self.order.id}"


class PartNotifyRequest(models.Model):
    """Stores a request to be notified when an out-of-stock part is restocked."""
    part = models.ForeignKey(VehiclePart, on_delete=models.CASCADE, related_name='notify_requests')
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('part', 'email')
        indexes = [
            models.Index(fields=['part', 'email']),
        ]

    def __str__(self):
        return f"Notify {self.email} when {self.part.name} is back in stock"


class PartReview(models.Model):
    """User review/comment on a vehicle part, including optional image upload."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    part = models.ForeignKey(VehiclePart, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('part', 'user_email')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} — {self.part.name} ({self.rating}\u2605)"