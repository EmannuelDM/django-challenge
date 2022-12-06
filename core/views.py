from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.filters import PropertyFilter, BookingFilter
from core.models import Property, PricingRule, Booking
from core.pagination import StandardResultsSetPagination
from core.serializers import PropertySerializer, PricingRuleSerializer, BookingSerializer
from core.service import BookingService


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter
    permission_classes = [IsAuthenticated]


class PricingRuleViewSet(viewsets.ModelViewSet):
    serializer_class = PricingRuleSerializer
    queryset = PricingRule.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking_service = BookingService()
        final_price = booking_service.calculate_final_price(
            request.data.get('property'),
            request.data.get('date_start'),
            request.data.get('date_end')
        )
        serializer.validated_data['final_price'] = final_price
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        booking = self.get_object()
        serializer = self.get_serializer(booking, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        booking_service = BookingService()
        property_id = request.data.get('property') or booking.property.id
        date_start = request.data.get('date_start') or booking.date_start.strftime("%m-%d-%Y")
        date_end = request.data.get('date_end') or booking.date_end.strftime("%m-%d-%Y")
        final_price = booking_service.calculate_final_price(
            property_id, date_start, date_end
        )
        serializer.validated_data['final_price'] = final_price
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


