from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view
# Create your views here.
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer,StorySerializer,TypeStorySerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import User,TypeStory
from rest_framework.permissions import AllowAny
# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#     def post(self, request, *args, **kwargs):
#         try:
#           serializer = self.get_serializer(data=request.data)
#           serializer.is_valid(raise_exception=True)
#           self.perform_create(serializer)
#           headers = self.get_success_headers(serializer.data)

#         # Tạo token
#           user = serializer.instance
#           jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#           jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#           access_token_payload = jwt_payload_handler(user)
#           access_token = jwt_encode_handler(access_token_payload)
# # Tạo token làm mới (refresh token)
#           refresh_token_payload = {'user_id': user.id}
#           refresh_token = jwt_encode_handler(refresh_token_payload)

#           return Response(
#             {'access_token': access_token, 'refresh_token': refresh_token},
#             status=status.HTTP_201_CREATED,
#             headers=headers
#                )
#         except Exception as e:
#                return Response(status=status.HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
def generate_tokens(user):
        # Tạo refresh token
        refresh = RefreshToken.for_user(user)

        # Tạo access token
        access_data = {'user_id': user.id, 'username': user.username}
        access_serializer = TokenObtainPairSerializer(data=access_data)
        access_serializer.is_valid(raise_exception=True)
        access = access_serializer.validated_data

        return access['access'], refresh
User = get_user_model()

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Kiểm tra xem username đã tồn tại hay chưa
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Kiểm tra xem email đã tồn tại hay chưa
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Tạo người dùng mới
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        # Xác thực thành công, tạo access token và refresh token
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)
    else:
        # Xác thực thất bại
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_user(request):
    refresh_token = request.data.get('refresh_token')

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

import jwt
def get_refresh_token(request):
    access_token = request.GET.get('access_token', None)
    
    if not access_token:
        return JsonResponse({'error': 'Access token is missing'}, status=400)

    try:
        payload = jwt.decode(access_token, verify=False)
        refresh_token = payload.get('refresh_token')
        
        if refresh_token:
            return JsonResponse({'refresh_token': refresh_token}, status=200)
        else:
            return JsonResponse({'error': 'Refresh token not found'}, status=400)
    except jwt.DecodeError:
        return JsonResponse({'error': 'Invalid access token'}, status=400)
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
@api_view(['POST'])
def reset_password_confirm_view(request, uidb64, token):
    
    print(request.data.get('new_password'))
    print(uidb64, token)
    uid =force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)
  
    if default_token_generator.check_token(user, token):
        # Xác nhận token hợp lệ, thay đổi mật khẩu
        new_password = request.data.get('new_password')
        print(new_password)
        user.set_password(new_password)
        print(user)
        user.save()
    
    
        return Response({'message': 'Password reset successfully'})

    return Response({'message': 'Invalid token'}, status=400)

import smtplib
from email.message import EmailMessage
import ssl
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
@api_view(['POST'])
def reset_password(request):
# Thông tin tài khoản email
    email = 'nguyentuandat1601@gmail.com'
    password = 'jdnfitzzxcbhzlxd'
    em  = EmailMessage()
# Thông tin người nhận và nội dung email
    email_recipient = request.data.get('email')
    
    User = get_user_model()

    try:
        user = User.objects.get(email=email_recipient)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Tạo token để reset mật khẩu
    token_generator = default_token_generator
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    reset_another = request.build_absolute_uri(reverse('reset_password_confirm', kwargs={'uidb64': user.pk, 'token': token}))
    reset_password_url = reset_password_url = f"http://localhost:3000/reset-password/{uid}/{token}/"
    # Gửi email chứa link reset mật khẩu
    email_subject = 'Password Reset'
    email_message = f'Please click the following link to reset your password: {reset_password_url} \n and check this {reset_another}'
    # send_mail(email_subject, email_message, 'noreply@example.com', [email])
    # subject = 'Subject of the Email'
    # message = 'Content of the Email'

    port = 465  # For starttls
    smtp_server = "smtp.gmail.com"
    em['From'] = email
    em['To'] = email_recipient
    em['Subject'] = email_subject
    em.set_content(email_message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context = context) as smtp:
        smtp.login(email,password=password)
        smtp.sendmail(email,email_recipient,em.as_string())
        

    return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
# class UserLoginView(JSONWebTokenAPIView):
#     serializer_class = JSONWebTokenSerializer

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Xác thực thông tin người dùng
#         user = authenticate(request, username=username, password=password)
#         if user:
#             # Tạo token truy cập (access token)
#             jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#             jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             return Response({'token': token})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



# class HomeView(APIView): 
# 	permission_classes = (IsAuthenticated, )
# 	def get(self, request):
# 		content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
# 		return Response(content)
# class LogoutView(APIView):
#      permission_classes = (IsAuthenticated,)
#      def post(self, request):
          
#           try:
#                refresh_token = request.data["refresh_token"]
#                token = RefreshToken(refresh_token)
#                token.blacklist()
#                return Response(status=status.HTTP_205_RESET_CONTENT)
#           except Exception as e:
#                return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def getAuthor(request):
	if request.method == 'GET':
		authorList = User.objects.all()
		serializers = UserSerializer(authorList, many=True)
		return JsonResponse(serializers.data,safe=False)
@api_view(['GET'])
def getTypeStory(request):
    if request.method == 'GET':
        ListType = TypeStory.objects.all()
        serializers = TypeStorySerializer(ListType, many=True)
        return JsonResponse(serializers.data,safe=False)
        # return Response({'values': serializers.data}, status=status.HTTP_200_OK)
from check.thotuc_text import checkthotuc
@api_view(['POST'])
def create_longstory(request):
    serializer = StorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)