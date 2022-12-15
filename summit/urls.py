from django.urls import path
from . import views

app_name = 'summit'
urlpatterns = [
    path('', views.main, name='main'),
    path('user_info/', views.user_info, name='user_info'),
    path('<int:id>/details', views.details, name='details'),
    path('user_form/', views.user_form, name= 'user_form'),
]

# href="{% url 'summit:user_info' %}"

