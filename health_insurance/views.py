from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import HealthPolicy, Dependent, HealthHistory
from .forms import HealthPolicyForm, DependentForm, HealthHistoryForm


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
                'hmo': Decimal("300.00"),
                'ppo': Decimal("350.00"),
                'epo': Decimal("330.00")
            }
            policy.premium_amount = plan_rates.get(policy.plan_type, Decimal("200.00")) * 28
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


@login_required
def add_health_history(request, policy_id):
    policy = get_object_or_404(HealthPolicy, id=policy_id, user=request.user)

    try:
        history = request.user.health_history
    except HealthHistory.DoesNotExist:
        history = None

    if request.method == 'POST':
        form = HealthHistoryForm(request.POST, instance=history)
        if form.is_valid():
            history = form.save(commit=False)
            history.user = request.user
            history.save()
            return redirect('health_insurance:quote_summary', policy_id=policy.id)
    else:
        form = HealthHistoryForm(instance=history)

    return render(request, 'health_insurance/add_health_history.html', {
        'form': form,
        'policy': policy
    })


@login_required
def quote_summary(request, policy_id):
    policy = get_object_or_404(HealthPolicy, id=policy_id, user=request.user)
    dependents = policy.dependents.all()

    try:
        health_history = request.user.health_history
    except HealthHistory.DoesNotExist:
        health_history = None

    context = {
        'policy': policy,
        'dependents': dependents,
        'health_history': health_history,
    }
    return render(request, 'health_insurance/quote_summary.html', context)
