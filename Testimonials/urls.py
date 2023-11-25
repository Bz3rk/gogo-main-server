from django.urls import path
from .views import TestimonialListView, TestimonialDetailView, TestimonialCreateView

urlpatterns = [
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('testimonials/<int:pk>/', TestimonialDetailView.as_view(), name='testimonial-detail'),
    path('testimonials/create', TestimonialCreateView.as_view(), name='testimonial-create'),
]
