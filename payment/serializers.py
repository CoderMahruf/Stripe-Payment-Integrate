from rest_framework import serializers
from .models import Subscription,Feature,Order

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['plan_name','price','description','button_text']


class FeatureSerializer(serializers.ModelSerializer):
    subscription = serializers.StringRelatedField()
    class Meta:
        model = Feature
        fields = ['id','subscription','name']