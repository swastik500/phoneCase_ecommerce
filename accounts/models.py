from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='India')
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_name}, {self.city}"

    def save(self, *args, **kwargs):
        # If this is set as default, unset others
        if self.is_default:
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)