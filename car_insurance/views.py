from django.shortcuts import render, redirect
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from decimal import Decimal

from .models import CarPolicy
from .forms import VehicleForm, CarPolicyForm

def apply_for_car_insurance(request):
    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)
        policy_form = CarPolicyForm(request.POST)

        if vehicle_form.is_valid() and policy_form.is_valid():
            # Save vehicle
            vehicle = vehicle_form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()

            # Calculate premium
            premium = Decimal("200") + (vehicle.value * Decimal("0.015"))

            # Save policy
            policy = policy_form.save(commit=False)
            policy.user = request.user
            policy.vehicle = vehicle
            policy.policy_number = f"AUTO{vehicle.id:05d}"
            policy.premium_amount = premium
            policy.start_date = timezone.now().date()
            policy.end_date = policy.start_date + timedelta(days=365)
            policy.is_active = False  # activate after payment
            policy.save()

            return redirect('car_insurance:quote_confirmation', policy_id=policy.id)

    else:
        vehicle_form = VehicleForm()
        policy_form = CarPolicyForm()

    return render(request, 'car_insurance/application_form.html', {
        'vehicle_form': vehicle_form,
        'policy_form': policy_form
    })


def quote_confirmation(request, policy_id):
    policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)

    return render(request, 'car_insurance/quote_confirmation.html', {
        'policy': policy,
        'vehicle': policy.vehicle,
    })