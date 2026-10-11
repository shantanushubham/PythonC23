# I want to create a serializer for the Task model.

from typing import override
from rest_framework import serializers
from .models import Task, User


# serializers.Serializer is a class that helps to convert the model instances to JSON and vice versa.
# class TaskSerializer(serializers.Serializer):
# id = serializers.IntegerField(read_only=True)
# title = serializers.CharField(max_length=200, error_messages={
#     "blank": "ದಯವಿಟ್ಟು ಶೀರ್ಷಿಕೆ ಯನ್ನು ಸೇರಿಸಿ.",
#     "required": "Abey Title bhi de",
# })
# description = serializers.CharField(max_length=200)
# completed = serializers.BooleanField(default=False)
# created_at = serializers.DateTimeField(read_only=True)
# updated_at = serializers.DateTimeField(read_only=True)
# # read_only: The field is read-only and cannot be modified.

# @override
# def create(self, validated_data: dict):
#     return Task.objects.create(**validated_data)

# @override
# def update(self, instance: Task, validated_data: dict):
#     # We are only updating the fields that are provided in the request. This is a partial update.
#     instance.title = validated_data.get("title", instance.title)
#     instance.description = validated_data.get("description", instance.description)
#     instance.completed = validated_data.get("completed", instance.completed)
#     instance.save()
#     return instance


class TaskSerializer(serializers.ModelSerializer):

    class Meta:  # Meta class is used to provide additional information about the serializer.
        model = Task  # The model that the serializer is associated with.
        fields = "__all__"  # The fields that will be serialized.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TaskUserSerializer(serializers.Serializer):

    user = UserSerializer(read_only=True)
    task_list = TaskSerializer(many=True, read_only=True)
    # read_only=True means that the field is read-only and cannot be modified.
