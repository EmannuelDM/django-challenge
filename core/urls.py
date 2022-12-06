
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from core.views import PropertyViewSet, PricingRuleViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'property', PropertyViewSet, basename='property')
router.register(r'pricing-rule', PricingRuleViewSet, basename='pricing-rule')
router.register(r'booking', BookingViewSet, basename='booking')


urlpatterns = [
    path(r'core/', include(router.urls)),
]
