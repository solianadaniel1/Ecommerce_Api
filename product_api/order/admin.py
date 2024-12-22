from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','quantity', 'order_status','shipping_address']  
    search_fields = ['user', 'product', 'quantity', 'order_status', 'shipping_address']
    list_filter = ['user', 'product','order_status']  
    readonly_fields = ['updated_at','created_at'] 

    
admin.site.register(Order, OrderAdmin)
