from django.contrib import admin
from apps.bill.models import BillingSetting, BillOrder, BillReturnedOrder


class BillOrderAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'order',
		'response_code',
		'issue_datetime'
	]
	list_filter = [
		'order__restaurant',
	]


admin.site.register(BillingSetting)
admin.site.register(BillOrder, BillOrderAdmin)
admin.site.register(BillReturnedOrder, BillOrderAdmin)
