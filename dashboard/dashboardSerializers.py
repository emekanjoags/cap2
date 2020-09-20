from rest_framework import serializers
from .models import Receivers, ReservedReceivers

class MakeDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivers
        fields = '__all__'

class MakeDonationBSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivers
        fields = '__all__'

class ReservedReceiversSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedReceivers
        fields = '__all__'
