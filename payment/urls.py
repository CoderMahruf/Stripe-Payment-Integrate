from django.urls import path
from .views import SubscriptionListView,CheckoutView,SubscriptionListAPIView,FeatureAPIView,CreatePaymentApiView,CreatePaymentView,StripeWebhookView, payment_success, payment_cancel

urlpatterns = [
    path('subscription',SubscriptionListView.as_view(),name='subscription'),
    path('checkout/<int:subscription_id>/',CheckoutView.as_view(),name='checkout'),

    path('create-payment/<int:subscription_id>/',CreatePaymentView.as_view(),name='create-payment'),
    path('stripe-webhook/',StripeWebhookView.as_view(),name='stripe-webhook'),

    path('success/', payment_success, name='success'),
    path('cancel/', payment_cancel, name='cancel'),

    # for api 
    path('api/subscription',SubscriptionListAPIView.as_view()),
    path('api/subscription/feature',FeatureAPIView.as_view()),
    path('api/create-payment/<int:subscription_id>/',CreatePaymentApiView.as_view(),name='create-payment'),
]
