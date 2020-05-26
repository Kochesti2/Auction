from functools import partial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from products.models import  Product
from users.models import Profile

User = get_user_model()

class RegisterForm(forms.Form):
    # username = forms.CharField()
    first_name = forms.CharField()
    last_name  = forms.CharField()
    email      = forms.EmailField()
    phone_number  = forms.CharField(required=False)
    password   = forms.CharField(widget=forms.PasswordInput)
    password2  = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must match.")
        return data


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',) #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class new_auction_form(forms.Form):
    name    = forms.CharField()
    description  = forms.CharField(widget=forms.Textarea)
    price      = forms.DecimalField(decimal_places=2,max_digits=10)
    min_increment  = forms.DecimalField(decimal_places=2,max_digits=10)
    end_date = forms.DateField(widget=DateInput())

# class AuctionForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name','description','price','min_increment','end_date'] #make sure to mention field here, if nothing is mentioned then all will be required.
#
# class NoteFullForm(AuctionForm): #extending form
#     images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#
#     class Meta(AuctionForm.Meta):
#         fields = AuctionForm.Meta.fields + ['images',]


# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Image')
#     class Meta:
#         model = ProductImages
#         fields = ('image', )


class Profile_user_form(forms.ModelForm):
    country    = forms.CharField()
    city    = forms.CharField()
    street      = forms.CharField()
    zip_code  = forms.CharField()
    photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['country', 'city', 'street','zip_code','photo']

