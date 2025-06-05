from django.shortcuts import render, get_object_or_404, redirect
from car_insurance.models import CarPolicy
from .forms import PaymentForm


def make_payment(request, policy_id):
    policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.policy_number = policy.policy_number
            payment.amount = policy.premium_amount
            payment.save()

            # Mark policy as active
            policy.is_active = True
            policy.save()

            return redirect('payments:payment_success', policy_id=policy.id)
    else:
        form = PaymentForm()

    return render(request, 'payments/make_payment.html', {
        'policy': policy,
        'form': form
    })


def payment_success(request, policy_id):
    policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)
    return render(request, 'payments/payment_success.html', {'policy': policy})
