from django.contrib import admin
from django.urls import path, include
from registration import views

#The docs view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Testimonials.urls')),
    path('api/', include('booking_summary.urls')),
    path('api/client-login/', views.ClientLogin),
    path('api/driver-login/', views.DriverLogin),
    path('api/client-register/', views.ClientRegister),
    path('api/driver-register/', views.DriverRegister),
    path('api/auth/', views.test_token),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


