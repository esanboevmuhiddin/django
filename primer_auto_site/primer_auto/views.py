from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *

def index(request):
    """Главная страница"""
    recent_orders = Order.objects.all()[:6]
    reviews = Review.objects.all()[:3]
    completed_orders = Order.objects.filter(status='completed').count()
    
    context = {
        'recent_orders': recent_orders,
        'reviews': reviews,
        'completed_orders': completed_orders,
    }
    return render(request, 'primer_auto/index.html', context)

def create_order(request):
    """Создание новой заявки"""
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        order_form = OrderForm(request.POST)
        
        if client_form.is_valid() and order_form.is_valid():
            try:
                # Сохраняем клиента
                client = client_form.save()
                # Сохраняем заявку, привязывая к клиенту
                order = order_form.save(commit=False)
                order.client = client
                order.save()
                
                messages.success(request, 
                    f'Заявка #{order.id} успешно создана! Мы свяжемся с вами в ближайшее время.')
                return redirect('order_detail', order_id=order.id)
                
            except Exception as e:
                messages.error(request, f'Произошла ошибка при создании заявки: {str(e)}')
    else:
        client_form = ClientForm()
        order_form = OrderForm()
    
    context = {
        'client_form': client_form,
        'order_form': order_form,
    }
    return render(request, 'primer_auto/create_order.html', context)

def order_detail(request, order_id):
    """Детальная информация о заявке"""
    order = get_object_or_404(Order, id=order_id)
    cars = Car.objects.filter(order=order)
    stages = OrderStage.objects.filter(order=order)
    payments = Payment.objects.filter(order=order)
    
    # Проверяем, есть ли отзыв для этого заказа
    has_review = Review.objects.filter(order=order).exists()
    
    context = {
        'order': order,
        'cars': cars,
        'stages': stages,
        'payments': payments,
        'has_review': has_review,
    }
    return render(request, 'primer_auto/order_detail.html', context)

def order_tracking(request, order_id):
    """Отслеживание заказа для клиента"""
    order = get_object_or_404(Order, id=order_id)
    stages = OrderStage.objects.filter(order=order).order_by('updated_date')
    
    # Рассчитываем прогресс
    total_stages = stages.count()
    completed_stages = stages.filter(is_completed=True).count()
    progress = int((completed_stages / total_stages) * 100) if total_stages > 0 else 0
    
    context = {
        'order': order,
        'stages': stages,
        'progress': progress,
    }
    return render(request, 'primer_auto/order_tracking.html', context)

def add_review(request, order_id):
    """Добавление отзыва к заказу"""
    order = get_object_or_404(Order, id=order_id)
    
    # Проверяем, есть ли уже отзыв для этого заказа
    if Review.objects.filter(order=order).exists():
        messages.warning(request, 'Отзыв для этого заказа уже существует')
        return redirect('order_detail', order_id=order.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = order.client
            review.order = order
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('order_detail', order_id=order.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'primer_auto/add_review.html', context)

def catalog(request):
    """Каталог подобранных автомобилей"""
    cars = Car.objects.all().order_by('-year')
    # Фильтрация
    brand = request.GET.get('brand')
    country = request.GET.get('country')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    
    if brand:
        cars = cars.filter(brand__icontains=brand)
    if country:
        cars = cars.filter(auction_country=country)
    if year_min:
        cars = cars.filter(year__gte=year_min)
    if year_max:
        cars = cars.filter(year__lte=year_max)
    
    # Получаем уникальные бренды для фильтра
    brands = Car.objects.values_list('brand', flat=True).distinct()
    
    context = {
        'cars': cars,
        'brands': brands,
        'selected_brand': brand,
        'selected_country': country,
        'selected_year_min': year_min,
        'selected_year_max': year_max,
    }
    return render(request, 'primer_auto/catalog.html', context)

def about(request):
    """Страница о компании"""
    return render(request, 'primer_auto/about.html')

def contacts(request):
    """Страница контактов"""
    return render(request, 'primer_auto/contacts.html')