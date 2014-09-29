from .forms import RealCostForm
from django.shortcuts import render
from decimal import Decimal

def home(request):
    if request.method == 'POST':
        form = RealCostForm(request.POST)
        if form.is_valid():
            # get form values
            net_price = form.cleaned_data['net_price']

            rebate = form.cleaned_data['rebate']

            bank_borrowing_rate = form.cleaned_data['bank_borrowing_rate'] / Decimal(100)
            bank_compounding_period = Decimal(form.cleaned_data['bank_compounding_period'])

            dealership_borrowing_rate = form.cleaned_data['dealership_borrowing_rate'] / Decimal(100)
            dealership_compounding_period = Decimal(form.cleaned_data['dealership_compounding_period'])

            months_borrowed = form.cleaned_data['months_borrowed']

            # calc values
            TERM_YEARS = Decimal(months_borrowed)/Decimal(12)

            bank_total_cost = round((net_price - rebate) * ((1 + bank_borrowing_rate/bank_compounding_period)**(bank_compounding_period*TERM_YEARS)), 2)
            dealership_total_cost = round(net_price * ((1 + dealership_borrowing_rate/dealership_compounding_period)**(bank_compounding_period*TERM_YEARS)), 2)

            real_interest_rate = round((dealership_compounding_period * ((Decimal(dealership_total_cost)/(net_price - rebate)) ** (1 / (dealership_compounding_period * TERM_YEARS)) - 1)) + (dealership_borrowing_rate * 100), 2)

            bank_total_interest_dollars = round(Decimal(bank_total_cost) - (net_price - rebate), 2)
            dealership_total_interest_dollars = round(Decimal(dealership_total_cost) - (net_price - rebate), 2)

            return render(request, 'home.html', {'form': form,
                                                 'bank_total_cost': bank_total_cost,
                                                 'dealership_total_cost': dealership_total_cost,
                                                 'bank_total_interest_dollars': bank_total_interest_dollars,
                                                 'dealership_total_interest_dollars': dealership_total_interest_dollars,
                                                 'real_interest_rate': real_interest_rate})
    else:
        form = RealCostForm()
    return render(request, 'home.html', {'form': form})
