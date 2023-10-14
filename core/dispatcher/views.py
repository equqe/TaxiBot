from rest_framework import generics as gen
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions as per

from dispatcher import serializers as ser


class RegisterDriverView(gen.CreateAPIView):
    serializer_class = ser.DriverAuthenticateSerializer
    permission_classes = [per.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)