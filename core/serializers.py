import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Property, PricingRule, Booking


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ['name', 'base_price']


class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = [
            'property',
            'price_modifier',
            'min_stay_length',
            'fixed_price',
            'specific_day'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['property'] = instance.property.name
        return ret


class BookingSerializer(serializers.ModelSerializer):
    date_start = serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y'])
    date_end = serializers.DateField(format="%m-%d-%Y", input_formats=['%m-%d-%Y'])
    final_price = serializers

    class Meta:
        model = Booking
        fields = [
            'property',
            'date_start',
            'date_end',
            'final_price'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['final_price'] = instance.final_price
        ret['property'] = instance.property.name
        return ret
