from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subscription(models.Model):
    plan_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    stripe_price_id = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name
    
class Feature(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="features")
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.text} ({self.subscription})"


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    is_paid = models.BooleanField(default=False)
    stripe_checkout_session_id = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.subscription.plan_name}"


