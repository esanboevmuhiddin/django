from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('catalog/', views.catalog, name='catalog'),
    path('create-order/', views.create_order, name='create_order'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/tracking/', views.order_tracking, name='order_tracking'),
    path('order/<int:order_id>/review/', views.add_review, name='add_review'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)