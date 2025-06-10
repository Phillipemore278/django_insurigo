from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required

from car_insurance.models import CarPolicy
from health_insurance.models import HealthPolicy,  HealthHistory
from claims.models import Claim
from quote.forms import QuoteForm


@login_required
def user_dashboard_view(request):
    policy_list = CarPolicy.objects.filter(user=request.user)
    policy_count = policy_list.count()
    car_premium_summary = sum(list.premium_amount for list in policy_list)
    claim_count = Claim.objects.filter(user=request.user).count()
    current_date = datetime.now().strftime("%A, %b %d, %Y")
    context = {
        'current_date':current_date,
        'policy_count': policy_count,
        'claim_count': claim_count,
        'car_premium_summary': car_premium_summary
    }
    return render(request, 'customer/user_dashboard.html', context)


@login_required
def my_policies(request):
    car_policies = CarPolicy.objects.filter(user=request.user)
    health_policies = HealthPolicy.objects.filter(user=request.user)

    return render(request, 'customer/my_policies.html', {
        'car_policies': car_policies,
        'health_policies': health_policies,
    })


@login_required
def policy_detail(request, policy_type, policy_id):
    health_history = None  # Initialize here to avoid reference error
    
    if policy_type == 'car':
        policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)
        context = {'policy': policy, 'policy_type': policy_type}

    elif policy_type == 'health':
        policy = get_object_or_404(HealthPolicy, id=policy_id, user=request.user)
        try:
            health_history = HealthHistory.objects.get(user=request.user)
        except HealthHistory.DoesNotExist:
            health_history = None
        context = {
            'policy': policy,
            'policy_type': policy_type,
            'health_history': health_history
        }

    else:
        return render(request, '404.html', status=404)

    return render(request, 'customer/policy_detail.html', context)


@login_required
def my_claims(request):
    claims = Claim.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'customer/my_claims.html', {'claims': claims})


@login_required
def get_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            insurance_type = form.cleaned_data['insurance_type']

            if insurance_type == 'health':
                plan = form.cleaned_data['health_plan_type']
                dependents = form.cleaned_data['health_dependents'] or 0
                add_ons = form.cleaned_data['health_add_ons']

                base_premium = {'hmo': 300, 'ppo': 350, 'epo': 330}.get(plan, 0)
                dependents_cost = dependents * 100
                add_ons_cost = 70 if add_ons else 0
                total_premium = base_premium + dependents_cost + add_ons_cost + 180
                year_payment = total_premium * 12

                quote = {
                    'type': 'Health Insurance',
                    'details': {
                        'Plan': plan.upper(),
                        'Dependents': dependents,
                        'Add-Ons': 'Yes' if add_ons else 'No',
                    },
                    'premium': total_premium,
                    'year_payment':year_payment,
                }

            else:  # car insurance
                make = form.cleaned_data['car_make']
                model = form.cleaned_data['car_model']
                year = form.cleaned_data['car_year']
                driver_age = form.cleaned_data['car_driver_age']

                # Example premium calculation logic
                base_premium = 500
                age_surcharge = 200 if driver_age and driver_age < 25 else 0
                year_discount = -10 * max(0, 2025 - (year or 2025))

                total_premium = base_premium + age_surcharge + year_discount + 180
                year_payment = total_premium * 12

                quote = {
                    'type': 'Car Insurance',
                    'details': {
                        'Make': make,
                        'Model': model,
                        'Year': year,
                        'Driver Age': driver_age,
                    },
                    'premium': total_premium,
                    'year_payment':year_payment
                }

            return render(request, 'customer/quote_summary.html', {'quote': quote, 'form': form})

    else:
        form = QuoteForm()

    return render(request, 'customer/get_quote.html', {'form': form})


# def quote_summary(request):
#     quote = request.session.get('quote_data')

#     if not quote:
#         return redirect('quotes:get_quote')

#     return render(request, 'quotes/quote_summary.html', {'quote': quote})


