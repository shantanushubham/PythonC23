from typing import override
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

from rest_framework.views import APIView

from tasks.serializers import TaskSerializer
from .models import Task

# views.py is the file that contains the views for the tasks app.
# A view is a function that returns a response to a request.

# Create your views here.

# A view function that adds two numbers
# The view function takes a request object as an argument

TASK_FILE_PATH = "tasks/files/tasks.json"


@api_view(["GET"])
# localhost:8000/api/add-numbers/
def add_numbers(request):
    # Get the query parameters from the request
    try:
        a = float(request.query_params["a"])
        b = float(request.query_params["b"])
        # Add the numbers
        result = a + b
        # Returns a response object
        return Response({"sum": result})  # Creating a response object
    except:
        return Response(
            {"error": "Invalid numbers"}, status=status.HTTP_400_BAD_REQUEST
        )


# ******** TASKS - FILE READING ********
class TaskView(APIView):

    def __get_all_tasks(self):
        with open(TASK_FILE_PATH, "r") as file:
            return json.loads(file.read())  # Returns a list of tasks

    # GET request to get a task by id
    @override  # This is just a convention to override the method. It doesn't do anything.
    def get(self, request, id=None):
        try:
            if id is None:
                # SELECT * FROM tasks;
                tasks = Task.objects.all()
                serializer = TaskSerializer(tasks, many=True)
                serialized_data = serializer.data
                return Response(data=serialized_data)
            else:
                # Find the task with the given id in the database

                # SELECT * FROM tasks WHERE id = <task-id>;
                task = Task.objects.get(id=id)
                # The task info is going out of the backend in the response and thus, needs to be serialised.
                # TaskSerializer(task) is the instance of the TaskSerializer class that converts the task instance to a JSON object.
                # It also validates the data and returns a ValidationError if the data is invalid.
                serializer = TaskSerializer(task)
                serialized_data = serializer.data
                return Response(data=serialized_data)
        except Task.DoesNotExist:
            return Response(
                data={"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # POST request to create a new task
    @override  # This is just a convention to override the method. It doesn't do anything.
    def post(self, request):  # Cannot change the name of the method
        data = request.data
        serializer = TaskSerializer(data=data)
        if not serializer.is_valid():
            # serializer.errors is a dictionary of the errors in the data.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # Task.objects.create(**serializer.validated_data) is equivalent to serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT request to update a task
    @override  # This is just a convention to override the method. It doesn't do anything.
    def put(self, request, id):
        try:
            data = request.data
            task = Task.objects.get(id=id)
            # task is the instance of the Task model that we want to update.
            # data is the data that we want to update the task with.
            serializer = TaskSerializer(task, data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # DELETE request to delete a task
    @override  # This is just a convention to override the method. It doesn't do anything.
    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # PATCH request to update a task partially
    @override  # This is just a convention to override the method. It doesn't do anything.
    def patch(self, request, id):
        try:
            data = request.data
            task = Task.objects.get(id=id)
            # partial=True means that only the fields that are provided in the request will be updated.
            serializer = TaskSerializer(task, data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
