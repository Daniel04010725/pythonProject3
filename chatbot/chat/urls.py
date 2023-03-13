from django.urls import path
from . import views

urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),  # 포스트리스트실행
]
