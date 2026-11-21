from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD for users. Authentication (signup, login, tokens, password) lives in
    the `authentication` app under /api/auth/.

    GET/PUT/PATCH /api/users/me/ - current user's profile

    list/retrieve/update/destroy are restricted to the caller's own record;
    staff can see and manage everyone. User creation goes through
    `POST /api/auth/signup/`, so plain `POST /api/users/` is disabled.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(pk=user.pk)

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Use /api/auth/signup/ to create a user."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def perform_destroy(self, instance):
        # Soft delete: ledger data may reference the user.
        instance.is_active = False # soft delete - happening because of AbstractUser
        instance.save(update_fields=["is_active"])

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        if request.method == "GET":
            return Response(UserSerializer(request.user).data)
        serializer = UserSerializer(
            request.user, data=request.data, partial=request.method == "PATCH"
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
