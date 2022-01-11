from django.contrib import admin

# Register your models here.
from apps.bill.models import BillingSetting

admin.site.register(BillingSetting)
