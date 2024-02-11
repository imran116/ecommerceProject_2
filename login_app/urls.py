from login_app import views
from django.urls import path

app_name = 'login_app'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_user, name='login'),

]
