# I want to create a serializer for the Task model.

from typing import override
from rest_framework import serializers

from tasks.utils import BCryptPasswordUtil
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


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "created_at", "updated_at", "is_active"]
        read_only_fields = ["id", "created_at", "updated_at"]

    @override
    def create(self, validated_data: dict):
        # validated_data["password"] = BCryptPasswordUtil.hash_password(validated_data["password"])
        # return super().create(validated_data)

        password = validated_data.pop("password")
        user = User(**validated_data)
        if password:
            user.set_password(password) # This will hash the password and set it to the user.
        user.save()
        return user

    @override
    def update(self, instance: User, validated_data: dict):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:  # Meta class is used to provide additional information about the serializer.
        model = Task  # The model that the serializer is associated with.
        fields = ["id", "title", "description", "completed", "created_at", "updated_at", "user"]  # The fields that will be serialized.
        read_only_fields = ["id", "created_at", "updated_at"]

    @override
    def create(self, validated_data: dict):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
    

class TaskUserSerializer(serializers.Serializer):

    user = UserSerializer(read_only=True)
    task_list = TaskSerializer(many=True, read_only=True)
    # read_only=True means that the field is read-only and cannot be modified.


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
