from django.contrib import admin
from .models import Subscription,Order,Feature
# Register your models here.

class FeatureInline(admin.TabularInline):  # You can also use admin.StackedInline
    model = Feature
    extra = 1  # How many empty forms to show
    min_num = 1  # Minimum required
    max_num = 10  # Optional: limit max

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'price', 'created_at', 'updated_at')
    inlines = [FeatureInline]
    search_fields = ['plan_name']
    list_filter = ['created_at', 'updated_at']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('text', 'subscription')
    search_fields = ['text', 'subscription__plan_name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscription', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'subscription__plan_name', 'stripe_checkout_session_id')
    ordering = ('-created_at',)