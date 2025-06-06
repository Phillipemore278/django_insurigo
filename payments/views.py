from django.shortcuts import render, get_object_or_404, redirect
from car_insurance.models import CarPolicy
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Payment


@login_required
def make_payment(request, policy_type, policy_id):
    if policy_type == 'car':
        from car_insurance.models import CarPolicy
        policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)
    elif policy_type == 'health':
        from health_insurance.models import HealthPolicy
        policy = get_object_or_404(HealthPolicy, id=policy_id, user=request.user)
    else:
        return redirect('home')  # Or return an error page

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.policy_id = policy.id
            payment.policy_type = policy_type
            payment.amount = policy.premium_amount
            payment.success = True
            payment.save()

            policy.is_active = True
            policy.save()

            return redirect('payments:payment_success', policy_number=policy.policy_number)
    else:
        form = PaymentForm()

    return render(request, 'payments/make_payment.html', {
        'form': form,
        'policy': policy,
        'policy_type': policy_type,
    })


def payment_success(request, policy_number):
    return render(request, 'payments/payment_success.html', {
        'policy_number': policy_number,
    })
