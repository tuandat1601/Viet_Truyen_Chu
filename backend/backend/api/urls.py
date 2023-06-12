from django.urls import path
from . import views

urlpatterns = [
    path('api/get-refresh-token/', views.get_refresh_token, name='get_refresh_token'),
    path('api/auth/', views.getAuthor, name='get_refresh_token'),
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/logout/', views.logout_user, name='user-logout'),
    path('api/reset-password/', views.reset_password, name='reset_password'),
    path('api/reset-password/<str:uidb64>/<str:token>/',views.reset_password_confirm_view, name='reset_password_confirm'),
    path('api/story/create/', views.create_longstory, name='create_longstory'),
    path('api/story/typestory/', views.getTypeStory, name='get_typestory'),
]