from django import forms
from products.models import Product
from .models import Comment


class Increment_price_form(forms.ModelForm):
    final_price  = forms.DecimalField(required=True,max_digits=10,decimal_places=2,min_value=0, label='')
    class Meta:
        model = Product
        fields = ['final_price']


class CommentForm(forms.ModelForm):
    # body = forms.TextInput(required=False)
    class Meta:
        model = Comment
        fields = ('body',)
