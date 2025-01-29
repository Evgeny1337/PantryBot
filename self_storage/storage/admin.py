from django.contrib import admin
from .models import Cell, CellTariff, Client, Order, Warehouse

admin.site.register(Client)
admin.site.register(Cell)
admin.site.register(CellTariff)
admin.site.register(Warehouse)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'contacts', 'start_storage', 'end_storage')
    search_fields = ('client', 'contacts', 'start_storage', 'end_storage')

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('end_storage')