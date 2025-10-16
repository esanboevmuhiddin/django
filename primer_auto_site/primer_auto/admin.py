from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Car)
admin.site.register(OrderStage)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Manager)