from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)


class SellerRegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddPartForm(forms.Form):
    name = forms.CharField(max_length=100)
    number = forms.CharField(max_length=100)
    brand = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    price = forms.IntegerField(min_value=0)
    stock = forms.IntegerField(min_value=0)
    condition = forms.CharField(max_length=100)
    vehicle = forms.IntegerField()  # FK id
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)


class CheckoutForm(forms.Form):
    fname = forms.CharField(max_length=100)
    lname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
