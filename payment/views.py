from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription,Order,Feature
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# api 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubscriptionSerializer,FeatureSerializer
# Create your views here.

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
    



def payment_success(request):
    response = {
        'status': 'success',
        'message': 'Payment completed successfully.'
    }
    return JsonResponse(response, status=200)


def payment_cancel(request):
    response = {
        'status': 'cancelled',
        'message': 'Payment was cancelled by the user.'
    }
    return JsonResponse(response, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)

        # Create order
        order = Order.objects.create(
            user=request.user,
            subscription=subscription,
            amount=subscription.price
        )

        # Create Stripe Checkout session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(subscription.price * 100),  # in cents
                        'product_data': {
                            'name': subscription.plan_name,
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
        except stripe.error.StripeError as e:
            # Handle Stripe errors properly (e.g., logging or showing error page)
            return JsonResponse({'error': str(e)}, status=500)

        # Save session ID to order
        order.stripe_checkout_session_id = session.id
        order.save()

        return redirect(session.url)
