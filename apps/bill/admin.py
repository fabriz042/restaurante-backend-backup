from django.contrib import admin

# Register your models here.
from apps.bill.models import BillingSetting, BillOrder

admin.site.register(BillingSetting)
admin.site.register(BillOrder)
