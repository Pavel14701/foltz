from rest_framework import serializers
from services.models import Service, ServiceSection


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSection
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'