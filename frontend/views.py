from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'frontend/index.html')

def frontend_get_quote(request):
    if request.method == 'POST':
        messages.error(request, 'You need to register with us to be able to access the quote engine, Register with the form below. Registration is free')
        return redirect('account:register')
    pass

def about(request):
    return render(request, 'frontend/about.html')

def services(request):
    return render(request, 'frontend/services.html')
