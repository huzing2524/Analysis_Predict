from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


class Predict(APIView):
    """预测"""

    def get(self, request):
        return Response("OK", status=status.HTTP_200_OK)
