from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.NewHomework.as_view(), name='new'),
    path('get/<int:course>',
        views.GetHomework.as_view(), name='get'),
    path('update/', views.UpdateHomework.as_view(), name='Update'),
    path('delete/<int:homework>', views.DeleteHomework.as_view(), name='delete'),
    path('response/new/', views.UploadResponse.as_view(), name='response'),
    path('response/updte/', views.GradeResponse.as_view(), name='update_response'),
    path('response/grade/', views.GradeResponse.as_view(), name='grade_response'),
    path('details/<int:response>',
        views.GetHomeworkDetails.as_view(), name='details'),
    path('response/get/<int:response>',
        views.GetResponse.as_view(), name='response_details')    
]
