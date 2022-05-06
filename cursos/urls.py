from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.NewCourse.as_view(), name='new_c'),
    path('get/', views.GetUserCourses.as_view(), name='get'),
    path('update/', views.UpdateCourse.as_view(), name='update'),
    path('delete/<int:course>', views.DeleteCourse.as_view(), name='delete'),
    path('get/<int:course>', views.GetCourseDetails.as_view(), name='details'),
    path('get/all', views.GetAllAvailableCourses.as_view(), name='get_all'),
    path('enroll/', views.StudentEnroll.as_view(), name='enroll'),
    path('post/new/', views.NewPost.as_view(), name='new_post'),
    path('post/get/<int:course>', views.GetPosts.as_view(), name="getPosts"),
    path('post/get/one/<int:post>', views.GetPost.as_view(), name='getPost'),
    path('post/update/', views.UpdatePost.as_view(), name='UpdatePost'),
    path('post/delete/<int:post>', views.DeletePost.as_view(), name='deletePost')
]
