from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import HealthPolicy, Dependent
from .forms import HealthPolicyForm, DependentForm


def apply_for_health_insurance(request):
    if request.method == 'POST':
        form = HealthPolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.user = request.user
            policy.policy_number = f"HLT{request.user.id}{timezone.now().strftime('%Y%m%d%H%M%S')}"
            policy.start_date = timezone.now().date()
            policy.end_date = policy.start_date + timedelta(days=365)

            # Premium estimate based on plan
            plan_rates = {
                'hmo': Decimal("150.00"),
                'ppo': Decimal("250.00"),
                'epo': Decimal("300.00")
            }
            policy.premium_amount = plan_rates.get(policy.plan_type, Decimal("200.00"))
            policy.is_active = False
            policy.save()

            return redirect('health_insurance:add_dependents', policy_id=policy.id)
    else:
        form = HealthPolicyForm()

    return render(request, 'health_insurance/apply_policy.html', {'form': form})


def add_dependents(request, policy_id):
    policy = HealthPolicy.objects.get(id=policy_id, user=request.user)

    if request.method == 'POST':
        form = DependentForm(request.POST)
        if form.is_valid():
            dependent = form.save(commit=False)
            dependent.user = request.user
            dependent.save()
            policy.dependents.add(dependent)
            print('form is valid')

            return redirect('health_insurance:add_dependents', policy_id=policy.id)  # Allow adding multiple
    else:
        print('form not valid')
        form = DependentForm()

    dependents = policy.dependents.all()

    return render(request, 'health_insurance/add_dependents.html', {
        'form': form,
        'policy': policy,
        'dependents': dependents
    })
