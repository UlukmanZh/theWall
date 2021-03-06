from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registration', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('post_message',views.post_message),
    path('delete_message', views.delete_message),
    path('post_comment', views.post_comment),
    path('delete_comment', views.delete_comment)

]