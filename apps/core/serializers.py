from rest_framework import serializers
from .models import Employee, ErpUser, Position, Branch


class ErpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErpUser
        fields = ['id', 'last_name', 'first_name']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'full_name']


class EmployeeSerializer(serializers.ModelSerializer):
    user = ErpUserSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'position', 'branch', 'start_date', 'dismissed', 'end_date', 'vacancy']