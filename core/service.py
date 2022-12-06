from datetime import datetime, timedelta

from core.models import PricingRule, Property


class BookingService:
    """ This class is for the bussines logic related to a booking"""
    def __init__(self) -> None:
        pass

    def calculate_final_price(self, property_id: int, date_start: str, date_end: str) -> float:
        date_start = datetime.strptime(date_start, "%m-%d-%Y")
        date_end = datetime.strptime(date_end, "%m-%d-%Y")
        booking_stay_length = (date_end - date_start).days + 1
        base_price = Property.objects.get(id=property_id).base_price
        total = 0

        all_pricing_rules = PricingRule.objects.filter(property__id=property_id)
        min_stay_length_rule = all_pricing_rules.filter(
            min_stay_length__lte=booking_stay_length).order_by('-min_stay_length').first()

        for i in range(booking_stay_length):
            current_date = date_start + timedelta(days=i)
            rules_of_the_day = all_pricing_rules.filter(specific_day=current_date)
            specific_day_price_modifier_rule = rules_of_the_day.order_by('-price_modifier').first()
            specific_day_fixed_price_rule = rules_of_the_day.order_by('-fixed_price').first()

            if specific_day_fixed_price_rule:
                total += specific_day_fixed_price_rule.fixed_price
                continue

            if specific_day_price_modifier_rule:
                total += base_price + (specific_day_price_modifier_rule.price_modifier * base_price / 100)
                continue

            if min_stay_length_rule and min_stay_length_rule.fixed_price:
                total += min_stay_length_rule.fixed_price
                continue

            if min_stay_length_rule and min_stay_length_rule.price_modifier:
                total += base_price + (min_stay_length_rule.price_modifier * base_price / 100)
                continue

        return total




