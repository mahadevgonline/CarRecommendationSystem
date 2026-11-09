from django import forms
import re


def validate_password(password):
    """Basic validation for existing users updating profiles."""
    if len(password) < 6: return 'Password must be at least 6 characters long.'
    if len(password) > 20: return 'Password must be no more than 20 characters long.'
    return None

def validate_strict_password(password):
    """
    Extremely strict validation ONLY applied to new registrations
    Rules:
      - Minimum 8 characters
      - Maximum 20 characters
      - At least one uppercase letter (A-Z)
      - At least one number (0-9)
      - At least one special symbol
    """
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if len(password) > 20:
        return 'Password must be no more than 20 characters long.'
    if not re.search(r'[A-Z]', password):
        return 'Password must contain at least one uppercase letter (A-Z).'
    if not re.search(r'[0-9]', password):
        return 'Password must contain at least one number (0-9).'
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]', password):
        return 'Password must contain at least one special symbol (e.g. @, #, !).'
    return None


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        error = validate_strict_password(password)
        if error:
            raise forms.ValidationError(error)
        return password


class SellerRegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        error = validate_strict_password(password)
        if error:
            raise forms.ValidationError(error)
        return password


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
    password = forms.CharField(widget=forms.PasswordInput, required=False, max_length=20)

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        # Only validate if user actually typed something
        if password:
            error = validate_password(password)
            if error:
                raise forms.ValidationError(error)
        return password

