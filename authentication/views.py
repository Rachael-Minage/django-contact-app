from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics,status,views
from authentication.serializers import RegisterSerializer
from rest_framework.response import Response


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        context = {
            "success": "Account created successfully"
        }
        
        return Response(context,status=status.HTTP_201_CREATED)