from ..models.expenseModels import *
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data, exclude=None):
        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description',instance.description)
        instance.amount = validated_data.get('amount',instance.amount)
        instance.currency = validated_data.get('currency',instance.currency)
        instance.is_approved = validated_data.get('is_approved',instance.is_approved)
        instance.save()
        return instance
