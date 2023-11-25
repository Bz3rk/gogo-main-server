from django.urls import path
from .views import bookingReceipt, createBooking, junctionList, priceTableList, bookRide, rideSummary, userRideList, driverCars


urlpatterns = [
    path('bookings/create', createBooking, name ='createBooking'),
    path('bookings/<str:user_id>', bookingReceipt, name = 'bookingReceipt'),
    path('book-ride/', bookRide, name='bookRide'),
    path('junction-list/', junctionList, name='junctionList'),
    path('price-table-list/', priceTableList, name='priceTableList'),
    path('ride-summary/<int:ride_id>', rideSummary, name = ' rideSummary'),
    path('user-ride-list', userRideList, name = ' userRideList'),
    path('assign-car', driverCars, name = ' drivercars'),
]