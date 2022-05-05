from django.urls import path
from authentication import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name= 'signup'),
    path('login/', views.Login.as_view(), name= 'login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update/q/', views.UpatehasQ.as_view(), name='updateq'),
    path('update/', views.UpdateProfile.as_view(), name='update'),
    path('get/', views.getProfile.as_view(), name='get')

]
