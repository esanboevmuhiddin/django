from django import forms
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'phone', 'email', 'telegram_username']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@example.com'}),
            'telegram_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'}),
        }
        labels = {
            'full_name': 'Ваше полное имя',
            'phone': 'Телефон',
            'email': 'Email',
            'telegram_username': 'Telegram (необязательно)',
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['desired_model', 'year_min', 'year_max', 'budget_max', 'additional_wishes']
        widgets = {
            'desired_model': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Например: Toyota Camry, Hyundai Sonata'
            }),
            'year_min': forms.NumberInput(attrs={'class': 'form-control', 'min': '1990', 'max': '2030'}),
            'year_max': forms.NumberInput(attrs={'class': 'form-control', 'min': '1990', 'max': '2030'}),
            'budget_max': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '20000',
                'step': '1000'
            }),
            'additional_wishes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Любые дополнительные пожелания к автомобилю...'
            }),
        }
        labels = {
            'desired_model': 'Желаемая марка и модель',
            'year_min': 'Минимальный год выпуска',
            'year_max': 'Максимальный год выпуска',
            'budget_max': 'Максимальный бюджет (USD)',
            'additional_wishes': 'Дополнительные пожелания',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text', 'photo']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} звезд') for i in range(1, 6)], 
                                 attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'rating': 'Ваша оценка',
            'review_text': 'Текст отзыва',
            'photo': 'Фото автомобиля (необязательно)',
        }