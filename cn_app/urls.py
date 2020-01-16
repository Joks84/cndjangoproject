from django.urls import path
from .views import (index, AboutView, post_list, post_detail, history_list,
                    nature_list, expats_list, city_list, province_list, add_comment,
                    email_list_signup)


from cn_app import views

app_name = 'cn_app'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', AboutView.as_view(), name = 'about'),
    path('signup/', views.signup, name = 'signup'),
    path('login_user/', views.login_user, name = 'login_user'),
    path('post_list/', views.post_list, name = 'post_list'),
    path('subscribe/', views.email_list_signup, name = 'subscribe'),
    path('cities/', views.city_list, name = 'cities'),
    path('post_list/<int:pk>/', views.post_detail, name = 'post_detail'),
    path('post_list/<int:pk>/comment/', views.add_comment, name = 'comment'),
    path('provinces/', views.province_list, name = 'provinces'),
    path('expats/', views.expats_list, name = 'expats'),
    path('history/', views.history_list, name = 'history'),
    path('nature/', views.nature_list, name = 'nature'),    
]
