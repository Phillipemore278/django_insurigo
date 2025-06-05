from django.shortcuts import get_object_or_404, render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from car_insurance.models import CarPolicy

@login_required
def user_dashboard_view(request):

    current_date = datetime.now().strftime("%A, %b %d, %Y")
    context = {
        'current_date':current_date,
    }
    return render(request, 'customer/user_dashboard.html', context)


@login_required
def my_policies(request):
    policies = CarPolicy.objects.filter(user=request.user)
    return render(request, 'customer/my_policies.html', {'policies': policies})


@login_required
def policy_detail(request, policy_id):
    policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)
    return render(request, 'customer/policy_detail.html', {'policy': policy})
