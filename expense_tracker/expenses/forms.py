from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date']
