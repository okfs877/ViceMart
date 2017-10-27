from django import forms

class PriceForm(forms.Form):
    price = forms.FloatField(label="price", min_value=0)