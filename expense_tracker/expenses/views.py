from django.shortcuts import render, redirect
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'expenses/expense_list.html', {'expenses': expenses, 'total_expense': total_expense})

    # expenses = Expense.objects.filter(user=request.user)
    # total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # expenses_by_category = defaultdict(list)
    # for expense in expenses:
    #     expenses_by_category[expense.category].append(expense)

    # context = {
    #     'expenses_by_category': dict(expenses_by_category),  # Convert to a normal dict
    #     'total_expense': total_expense,
    #     'expense_categories': Expense.CATEGORY_CHOICES,
    # }
    
    # return render(request, 'expenses/expense_list.html', context)

@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    expense.delete()
    return redirect('expense_list')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically after registration
            return redirect('expense_list')  # Redirect to home page
    else:
        form = UserCreationForm()

    return render(request, 'expenses/register.html', {'form': form})



