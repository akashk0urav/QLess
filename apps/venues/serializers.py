from rest_framework import serializers
from .models import Venue, VenueMember
from apps.accounts.models import User    

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"