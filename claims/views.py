from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Claim
from .forms import ClaimForm
from car_insurance.models import CarPolicy
from health_insurance.models import HealthPolicy

@login_required
def file_claim(request, policy_type, policy_id):
    # Fetch policy to verify ownership
    if policy_type == 'car':
        policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)
    elif policy_type == 'health':
        policy = get_object_or_404(HealthPolicy, id=policy_id, user=request.user)
    else:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user
            claim.policy_type = policy_type
            claim.policy_id = policy.id
            claim.save()
            return redirect('claims:claim_success', claim_id=claim.id)
    else:
        form = ClaimForm()

    context = {
        'form': form,
        'policy': policy,
        'policy_type': policy_type,
    }
    return render(request, 'claims/file_claim.html', context)


@login_required
def claim_success(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id, user=request.user)
    return render(request, 'claims/claim_success.html', {'claim': claim})

