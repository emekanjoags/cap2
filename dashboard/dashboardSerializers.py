from rest_framework import serializers
from .models import Receivers, ReservedReceivers, Timer, Investor

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

class TimerSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Timer
        fields = '__all__'

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'