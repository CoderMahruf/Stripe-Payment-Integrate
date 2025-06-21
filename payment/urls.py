from django.urls import path
from .views import SubscriptionListView,CheckoutView,SubscriptionListAPIView,FeatureAPIView

urlpatterns = [
    path('subscription',SubscriptionListView.as_view(),name='subscription'),
    path('checkout/<int:subscription_id>/',CheckoutView.as_view(),name='checkout'),

    # for api 
    path('api/subscription',SubscriptionListAPIView.as_view()),
    path('api/subscription/feature',FeatureAPIView.as_view())
]
