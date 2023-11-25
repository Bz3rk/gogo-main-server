from rest_framework import generics
#from django.shortcuts import render
from .models import Testimonials
from .serializers import TestimonialsSerializer
from .permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class TestimonialListView(generics.ListAPIView):
   queryset = Testimonials.objects.all()
   serializer_class = TestimonialsSerializer


class TestimonialCreateView(generics.CreateAPIView):
   queryset = Testimonials.objects.all()
   serializer_class = TestimonialsSerializer
   permission_classes = [IsAuthenticated]

   def perform_create(self, serializer):
      serializer.save(author= self.request.user)


class TestimonialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testimonials.objects.all()
    serializer_class = TestimonialsSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdminOrReadOnly]
