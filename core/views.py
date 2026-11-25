
from django.shortcuts import render, redirect, get_object_or_404

from .models import Farmer, Produce, BuyerOrder
from .forms import FarmerForm, ProduceForm, BuyerOrderForm


def dashboard(request):
    context = {
        'farmer_count': Farmer.objects.count(),
        'produce_count': Produce.objects.filter(available=True).count(),
        'order_count': BuyerOrder.objects.count(),
        'farmers': Farmer.objects.all().order_by('-id')[:5],
        'produce': Produce.objects.filter(
            available=True
        ).order_by('-id')[:5],
        'orders': BuyerOrder.objects.all().order_by('-id')[:5],
    }

    return render(request, 'core/dashboard.html', context)


def add_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FarmerForm()

    return render(request, 'core/farmer_form.html', {'form': form})


def add_produce(request):
    if request.method == 'POST':
        form = ProduceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProduceForm()

    return render(request, 'core/produce_form.html', {'form': form})


def add_order(request):
    if request.method == 'POST':
        form = BuyerOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('match_order', order_id=order.id)
    else:
        form = BuyerOrderForm()

    return render(request, 'core/order_form.html', {'form': form})


def match_order(request, order_id):
    order = get_object_or_404(BuyerOrder, id=order_id)

    listings = Produce.objects.filter(
        available=True,
        crop_name__iexact=order.crop_name,
        price_per_kg__lte=order.target_price_per_kg
    ).select_related('farmer').order_by('price_per_kg', 'id')

    remaining = order.required_quantity_kg
    allocations = []
    total_cost = 0

    for item in listings:
        if remaining <= 0:
            break

        quantity = min(item.quantity_kg, remaining)
        cost = quantity * item.price_per_kg

        allocations.append({
            'farmer': item.farmer.name,
            'village': item.farmer.village,
            'crop': item.crop_name,
            'quantity': quantity,
            'price': item.price_per_kg,
            'cost': cost,
        })

        remaining -= quantity
        total_cost += cost

    matched_quantity = order.required_quantity_kg - remaining

    if remaining <= 0:
        status = 'Fully matched'
    elif matched_quantity > 0:
        status = 'Partially matched'
    else:
        status = 'No matching produce found'

    average_price = (
        total_cost / matched_quantity if matched_quantity > 0 else 0
    )

    context = {
        'order': order,
        'allocations': allocations,
        'matched_quantity': matched_quantity,
        'remaining': remaining,
        'total_cost': total_cost,
        'average_price': average_price,
        'status': status,
    }

    return render(request, 'core/matching.html', context)
