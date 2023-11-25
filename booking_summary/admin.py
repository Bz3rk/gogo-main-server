from django.contrib import admin
from .models import BookingSummary, Junction, Ride, PriceTable, Car

# Register your models here.

admin.site.register(BookingSummary)
admin.site.register(Junction)
admin.site.register(Ride)
admin.site.register(PriceTable)
admin.site.register(Car)
