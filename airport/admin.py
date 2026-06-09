from django.contrib import admin

from airport.models import AirplaneType, Airport, Airplane, Route, Crew, Flight, Order, Ticket

# Register your models here.
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(Flight)
admin.site.register(Ticket)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]