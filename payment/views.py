from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription,Order,Feature
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# api 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubscriptionSerializer,FeatureSerializer

class SubscriptionListView(View):
    def get (self,request):
        subscriptions = Subscription.objects.all( )
        return render(request,'payment.html',{'subscriptions':subscriptions})
#  api    
class SubscriptionListAPIView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Subscription.objects.all()
        serializer = SubscriptionSerializer(queryset,many=True)
        return Response({
            'status': 'success',
            "message": "Data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class CheckoutView(View):
    template_name = 'checkout.html'
    def get(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)
        features = subscription.features.all()
        return render(request, self.template_name, {
            'subscription': subscription,
            'features': features
        })


# api 
class FeatureAPIView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = Feature.objects.all()
        serializer = FeatureSerializer(queryset,many = True)
        return Response({
            'status': 'success',
            "message": "Data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)