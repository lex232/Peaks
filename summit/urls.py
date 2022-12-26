from django.urls import path
from . import views
from .views import RegisterView, profile



app_name = 'summit'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:id>/details', views.details, name='details'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]


