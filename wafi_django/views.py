from django.shortcuts import render
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def add_users(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        account = Account.objects.create(user=user, balance=0)
        account.save()

@login_required
def user_deposit_money(request):
    if request.method == 'POST':
        amount_to_be_deposited = request.POST.get('amount')
        user = Account.objects.get(user_id=request.user)
        user.balance += int(amount_to_be_deposited)
        user.save()

@login_required
def user_send_money(request):
    if request.method == 'POST':
        amount_to_be_sent = request.POST.get('amount')
        user_to_be_sent_money = request.POST.get('user_id')
        sender = Account.objects.get(user_id=request.user)
        receiver = Account.objects.get(user_id=user_to_be_sent_money)
        if sender.balance > amount_to_be_sent:
            sender.balance -= int(amount_to_be_sent)
            receiver.balance += int(amount_to_be_sent)
            sender.save()
            receiver.save()
        else: 
            return "Transaction is not possible"

@login_required    
def check_balance(request):
    if request.method == 'POST':
        user = Account.objects.get(user_id=request.user)
        return user.balance

@login_required
def transfer_money(request):
    if request.method == 'POST':
        amount_to_be_transferred = request.POST.get('amount')
        sender = Account.objects.get(user_id=request.user)
        if sender.balance > amount_to_be_transferred:
            sender.balance -= int(amount_to_be_transferred)
        else:
            return "Transaction is not possible"
        
        

