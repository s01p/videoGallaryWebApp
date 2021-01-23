from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    
    path("photogallary/",views.photogallary,name='photogallary'),
    path("downloadimage",views.export,name='export'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('photogallary/<slug:name>/remove/', views.photogallary_after_remove, name='photogallary_after_remove'),
    
]