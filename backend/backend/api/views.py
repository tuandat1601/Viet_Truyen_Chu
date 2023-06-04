from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import AuthorStory
from django.views.decorators.csrf import csrf_exempt
from .serializers import AuthorStorySerializers
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
class HomeView(APIView): 
	permission_classes = (IsAuthenticated, )
	def get(self, request):
		content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
		return Response(content)
class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def getAuthorStory(request):
	if request.method == 'GET':
		authorList = AuthorStory.objects.all()
		serializers = AuthorStorySerializers(authorList, many=True)
		
		
		return JsonResponse(serializers.data,safe=False)