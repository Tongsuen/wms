from django.contrib import admin
from .models import CarPath,Product,Order, OrderItem,PackagingType,RecieveProductAddress, OrderStatusChange, TransportWithOrderTransection, OrderTracking
# Register your models here.


admin.site.register(CarPath)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PackagingType)
admin.site.register(RecieveProductAddress)
admin.site.register(OrderStatusChange)
admin.site.register(TransportWithOrderTransection)
admin.site.register(OrderTracking)
