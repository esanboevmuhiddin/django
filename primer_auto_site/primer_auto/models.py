from django.db import models
from django.core.validators import *

class Client(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    telegram_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    
    def __str__(self):
        return f"{self.full_name} ({self.phone})"

class Manager(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    
    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
    
    def __str__(self):
        return self.full_name

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('searching', 'На подборе'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Менеджер")
    desired_model = models.CharField(max_length=100, verbose_name="Желаемая модель")
    year_min = models.PositiveIntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name="Минимальный год"
    )
    year_max = models.PositiveIntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name="Максимальный год"
    )
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Максимальный бюджет (USD)")
    additional_wishes = models.TextField(blank=True, null=True, verbose_name="Дополнительные пожелания")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new', verbose_name="Статус")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Заявка #{self.id} - {self.desired_model}"

class Car(models.Model):
    COUNTRY_CHOICES = [
        ('usa', 'США'),
        ('korea', 'Корея'),
        ('china', 'Китай'),
        ('europe', 'Европа'),
        ('japan', 'Япония'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заявка")
    lot_number = models.CharField(max_length=50, verbose_name="Номер лота")
    vin = models.CharField(max_length=17, verbose_name="VIN-номер")
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    auction_country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, verbose_name="Страна аукциона")
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Текущая ставка (USD)")
    photo = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Фото")
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

class OrderStage(models.Model):
    STAGE_CHOICES = [
        ('search', 'Подбор'),
        ('auction', 'Торг/Покупка'),
        ('shipping', 'Доставка'),
        ('customs', 'Таможня'),
        ('registration', 'Постановка на учет'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заявка")
    stage_name = models.CharField(max_length=20, choices=STAGE_CHOICES, verbose_name="Название этапа")
    is_completed = models.BooleanField(default=False, verbose_name="Завершен")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Этап заказа"
        verbose_name_plural = "Этапы заказа"
    
    def __str__(self):
        return f"{self.order} - {self.get_stage_name_display()}"

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('deposit', 'Предоплата'),
        ('auction', 'Оплата аукциона'),
        ('shipping', 'Оплата доставки'),
        ('customs', 'Оплата пошлины'),
        ('final', 'Финальный расчет'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заявка")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name="Тип платежа")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата платежа")
    
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
    
    def __str__(self):
        return f"Платеж #{self.id} - {self.get_payment_type_display()}"

class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заявка")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    review_text = models.TextField(verbose_name="Текст отзыва")
    review_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name="Фото автомобиля")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-review_date']
    
    def __str__(self):
        return f"Отзыв от {self.client.full_name} - {self.rating}"