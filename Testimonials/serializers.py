from rest_framework import serializers
from .models import Testimonials

class TestimonialsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Testimonials
        fields = ['id', 'author', 'body', 'created']
