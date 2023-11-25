from django.db import models
from django.conf import settings

# Create your models here.



CustomUser = settings.AUTH_USER_MODEL
class Testimonials(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:30]



