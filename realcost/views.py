from .forms import RealCostForm
from django.shortcuts import render
from decimal import Decimal
from scipy.optimize import newton


def rootfinding_amortization(i, P, n, A):
    return P*(i + (i/((1+i)**n - 1))) - A


def payment(principal, apr, number_of_periods):
    if apr == 0:
        periodic_payment = principal/number_of_periods
    else:
        monthly_interest_rate = apr/12
        periodic_payment = principal*(monthly_interest_rate + (monthly_interest_rate/((1+monthly_interest_rate)**number_of_periods - 1)))
    return round(periodic_payment, 2)


def home(request):
    if request.method == 'POST':
        form = RealCostForm(request.POST)
        if form.is_valid():

            # Gather and sanitize inputs.
            net_price = form.cleaned_data['net_price']
            rebate = form.cleaned_data['rebate']
            bank_apr = form.cleaned_data['bank_borrowing_rate'] / Decimal(100)
            dealership_apr = form.cleaned_data['dealership_borrowing_rate'] / Decimal(100)
            loan_periods = int(form.cleaned_data['months_borrowed'])


            # Calculated Values
            bank_principle = net_price - rebate


            # Monthly Payment Calculations
            bank_monthly_payment = payment(bank_principle, bank_apr, loan_periods)
            dealership_monthly_payment = payment(net_price, dealership_apr, loan_periods)


            # Total Cost Calculations
            bank_total_cost = bank_monthly_payment * loan_periods
            dealership_total_cost = dealership_monthly_payment * loan_periods


            # Effective Interest Cost Calculations
            # Cost of interest is normalized with respect to the rebated price.
            bank_total_interest_dollars = round(Decimal(bank_total_cost) - bank_principle, 2)
            dealership_total_interest_dollars = round(Decimal(dealership_total_cost) - bank_principle, 2)


            # Effective APR Calculation
            bank_apr = round(bank_apr * 100, 4)
            # Effective Dealership APR is calculated using Newton root-finding Method with initial approximation of the advertised APR
            # The root-finding library only works with floats.
            if dealership_apr == 0:
                # Avoid divide by zero error in root-finding method.
                # Approximate 0 for initial guess.
                initial_guess = 0.000000001
            else:
                # Use dealership_apr as initial guess for root-finding.
                # In most real-world cases, this should reasonably approximate the effective APR.
                initial_guess = dealership_apr

            # WARNING: Newton's root-finding method is NOT guaranteed to converge! In some unlikely cases, the method
            #          may fail to solve the equation. Use a bounded root-finding method if problems occur.
            effective_dealership_apr = round(12 * 100 * newton(rootfinding_amortization, float(initial_guess), args=(float(bank_principle), float(loan_periods), float(dealership_monthly_payment))), 4)


            # Return values to HTML page.
            # Dollar amounts are formatted to exactly two decimal places.
            return render(request, 'home.html', {'form': form,
                                                 'bank_total_cost': '%.2f' % bank_total_cost,
                                                 'dealership_total_cost': '%.2f' % dealership_total_cost,
                                                 'bank_total_interest_dollars': '%.2f' % bank_total_interest_dollars,
                                                 'dealership_total_interest_dollars': '%.2f' % dealership_total_interest_dollars,
                                                 'bank_monthly_payment': '%.2f' % bank_monthly_payment,
                                                 'dealership_monthly_payment': '%.2f' % dealership_monthly_payment,
                                                 'real_dealership_interest_rate': effective_dealership_apr,
                                                 'real_bank_interest_rate': bank_apr})
    else:
        form = RealCostForm()
    return render(request, 'home.html', {'form': form})