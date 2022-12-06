from rest_framework.throttling import AnonRateThrottle


class AuthAnonMinThrottle(AnonRateThrottle):
    rate = "10/min"
    scope = 'custom_per_min'
