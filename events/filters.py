from django_filters import rest_framework as filters
from .models import Event
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
import math

class EventFilter(filters.FilterSet):
    time_period = filters.CharFilter(method='filter_time_period')
    distance = filters.NumberFilter(method='filter_distance')
    user_lat = filters.NumberFilter(method='noop')
    user_long = filters.NumberFilter(method='noop')
    age_group = filters.ChoiceFilter(choices=[('3-5', '3-5 yrs'), ('6-8', '6-8 yrs'), ('9-12', '9-12 yrs')])
    price_type = filters.CharFilter(method='filter_price')
    status = filters.CharFilter(method='filter_status')

    class Meta:
        model = Event
        fields = ['age_group', 'admin']

    def noop(self, queryset, name, value):
        return queryset

    def filter_time_period(self, queryset, name, value):
        now = timezone.now()
        if value == 'today':
            return queryset.filter(time__date=now.date())
        elif value == 'this_weekend':
            # Assuming weekend is Saturday and Sunday
            saturday = now + timedelta(days=(5 - now.weekday()) % 7)
            sunday = saturday + timedelta(days=1)
            return queryset.filter(time__date__range=[saturday.date(), sunday.date()])
        return queryset

    def filter_status(self, queryset, name, value):
        now = timezone.now()
        if value == 'upcoming':
            return queryset.filter(time__gt=now)
        elif value == 'past':
            return queryset.filter(time__lt=now)
        return queryset

    def filter_price(self, queryset, name, value):
        if value == 'free':
            return queryset.filter(price=0)
        elif value == 'paid':
            return queryset.filter(price__gt=0)
        return queryset

    def filter_distance(self, queryset, name, value):
        user_lat = self.data.get('user_lat')
        user_long = self.data.get('user_long')
        
        if not (user_lat and user_long and value):
            return queryset

        user_lat = float(user_lat)
        user_long = float(user_long)
        distance_limit = float(value)

        # Basic bounding box filtering for performance before accurate haversine
        # 1 degree of latitude is approx 69 miles
        lat_range = distance_limit / 69.0
        # 1 degree of longitude is approx 69 * cos(lat) miles
        long_range = distance_limit / (69.0 * math.cos(math.radians(user_lat)))

        queryset = queryset.filter(
            latitude__range=(user_lat - lat_range, user_lat + lat_range),
            longitude__range=(user_long - long_range, user_long + long_range)
        )

        # For more accurate results, we could iterate or use GeoDjango, 
        # but bounding box is usually enough for simple cases.
        return queryset
