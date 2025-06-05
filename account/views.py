from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required

from .forms import CustomAuthenticationForm, CustomerRegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        next_url = request.GET.get('next') or request.POST.get('next')

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Handle 'remember me'
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            # Safe redirect
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                print('using next')
                return redirect(next_url)

            # Role-based fallback redirect
            if user.is_staff:
                messages.success(request, f'Welcome, {user.full_name}!')
                return redirect('account:admin_dashboard')
            else:
                return redirect('customer:user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
        next_url = request.GET.get('next')

    return render(request, 'account/login.html', {'form': form, 'next': next_url})


def register_view(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('account:login')  # Update with your actual login URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)  
    return redirect('account:login')

@login_required
def admin_dashboard_view(request):
    return render(request, 'account/admin_dashboard.html')