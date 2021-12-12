from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='stock_symbol', max_length=100)