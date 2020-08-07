from django.contrib.auth.models import User

from .models import Screen,Row,Seat

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ('id','screen_name')

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ('id','screen','row_name','number_of_seats','aisle_seats')

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id','screen','row','seat_number','is_reserved')