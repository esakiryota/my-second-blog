from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Solve


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solve
        fields = '__all__'